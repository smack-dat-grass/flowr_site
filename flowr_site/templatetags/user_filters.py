from django import template
register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    # print(f"checking {user} for {group_name}")
    return user.groups.filter(name=group_name).exists()
#check if a user has a group in a list of groups
@register.filter(name='has_groups')
def has_groups(user, groups):
    for group in groups:
        print(f"checking {user} for {group.name}")
        if user.groups.filter(name=group.name).exists():
            return True

    return False
