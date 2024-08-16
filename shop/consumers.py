class InteractionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'interactions'
        self.room_group_name = 'interactions_group'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_id = self.scope["user"].id
        product_id = data['product_id']

        if data['type'] == 'click':
            # Handle click interaction
            interaction, _ = Interaction.objects.get_or_create(user_id=user_id, product_id=product_id)
            interaction.clicks += 1
            interaction.save()

        elif data['type'] == 'time_spent':
            # Handle time spent interaction
            interaction, _ = Interaction.objects.get_or_create(user_id=user_id, product_id=product_id)
            interaction.time_spent += data['value']
            interaction.save()

        elif data['type'] == 'scroll':
            # Handle scroll depth interaction
            interaction, _ = Interaction.objects.get_or_create(user_id=user_id, product_id=product_id)
            interaction.scroll_depth = max(interaction.scroll_depth, data['value'])
            interaction.save()

        elif data['type'] == 'add_to_cart':
            # Handle add to cart interaction
            interaction, _ = Interaction.objects.get_or_create(user_id=user_id, product_id=product_id)
            interaction.add_to_cart = True
            interaction.save()

        # Update rating based on interactions
        rating = Rating.update_or_create_rating(user_id=user_id, product_id=product_id)

        # Send updated rating back to all connected clients
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'rating_update',
                'rating': str(rating.rating),
                'product_id': product_id
            }
        )

    async def rating_update(self, event):
        rating = event['rating']
        product_id = event['product_id']

        # Send updated rating to WebSocket
        await self.send(text_data=json.dumps({
            'rating': rating,
            'product_id': product_id
        }))
