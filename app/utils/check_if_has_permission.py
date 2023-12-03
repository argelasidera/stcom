from app.models.user import user_schema_factory


def check_if_has_permission(user, permission) -> bool:
    user_dump = user_schema_factory().dump(user)
    roles = user_dump.get("role")

    if not roles:
        return False

    if not roles.get("permissions"):
        return False

    has_permission = False

    for perm in roles.get("permissions"):
        # Check if the account has the linked permission
        if perm["slug"] == permission:
            has_permission = True
            break

    return has_permission
