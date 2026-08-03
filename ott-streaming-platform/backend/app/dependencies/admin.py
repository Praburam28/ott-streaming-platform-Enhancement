from fastapi import Depends, HTTPException, status

from app.core.security import get_current_user


def require_admin(
    current_user=Depends(get_current_user),
):
    """
    Allow access only to admin users.
    """

    if current_user.role.lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )

    return current_user