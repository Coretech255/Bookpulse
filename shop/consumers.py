from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
from .models import Product, Interaction, Rating
from .recommendation import load_data, train_algorithm, get_top_n_recommendations

class InteractionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join room
        self.room_group_name = f'user_{self.scope["user"].id}_interactions'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
            text_data_json = json.loads(text_data)
            isbn = text_data_json['isbn']
            action = text_data_json['action']
            user = self.scope['user']

            if user.is_authenticated:
                # Process interaction
                product = await sync_to_async(Product.objects.get)(isbn=isbn)

                interaction, created = await sync_to_async(Interaction.objects.get_or_create)(
                    user=user, product=product
                )
                rating_value = 0.0

                if action == 'like':
                    interaction.liked = True
                    rating_value = interaction.calculate_interaction_value()
                elif action == 'add_to_cart':
                    interaction.added_to_cart = True
                    rating_value = interaction.calculate_interaction_value()
                elif action == 'click':
                    interaction.clicks += 1
                    if 'time_spent' in text_data_json:
                        interaction.time_spent += float(text_data_json['time_spent'])
                        rating_value = interaction.calculate_interaction_value()

                await sync_to_async(interaction.save)()

                # Update or create the rating
                rating, created = await sync_to_async(Rating.objects.get_or_create)(
                    user=user, product=product
                )
                await sync_to_async(rating.update_rating)(rating_value)

                # Send the updated rating to the client
                await self.send(text_data=json.dumps({
                    'status': 'success',
                    'rating': rating.rating
                }))

                # Generate recommendations
                #data, df = await sync_to_async(load_data)()
                #algo = await sync_to_async(train_algorithm)(data)
                #recommendations = await sync_to_async(get_top_n_recommendations)(algo, user.id, df, n=10)

                #recommended_books = await sync_to_async(Product.objects.filter)(isbn__in=recommendations)
                #recommended_books_data = [
                ##    {'title': book.title, 'isbn': book.isbn} for book in recommended_books
                #]

                # Send recommendations to the client
                #await self.send(text_data=json.dumps({
                #    'status': 'success',
                #    'recommendations': recommended_books_data
                #}))
            else:
                await self.send(text_data=json.dumps({'status': 'error', 'message': 'User not authenticated'}))


    #def get_product(isbn):
     #   return sync_to_async(Product.objects.get)(isbn=isbn)

    #def get_or_create_interaction(user, product):
    #    return sync_to_async(Interaction.objects.get_or_create)(user=user, product=product)

    #def update_or_create_rating(user, product, rating_value):
    ##    rating, created = sync_to_async(Rating.objects.get_or_create)(user=user, product=product)
     #   sync_to_async(rating.update_rating)(rating_value)
     #   return rating

    #def get_recommended_books(recommendations):
    #    return sync_to_async(Product.objects.filter)(isbn__in=recommendations)
