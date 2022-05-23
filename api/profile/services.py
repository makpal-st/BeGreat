
def update_profile(user, data):
    if 'email' in data:
        user.email = data['email']
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'middle_name' in data:
        user.middle_name = data['middle_name']
    if 'region' in data:
        user.region = data['region']
    if 'phone' in data:
        user.phone = data['phone']
    if 'password' in data:
        user.set_password(data['password'])
    user.save()
    if 'avatar' in data:
        user.account.avatar = data['avatar']
        user.account.save()
    return user.account
