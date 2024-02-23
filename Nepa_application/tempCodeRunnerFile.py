user = User.objects.get(username='example_user')  # Replace 'example_user' with the username of the user you want to get comments for
total_comments = get_total_comments_for_user(user)
print(total_comments)  