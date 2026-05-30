import io
from typing import List
from fastapi import APIRouter, UploadFile, HTTPException, Body
from fastapi.responses import StreamingResponse
from letterboxd_scraper import retrive_watchlist_from_user
from watchlist_intersecter import intersect_watchlists

router = APIRouter()

@router.get("/{username}")
def get_watchlist(username: str, format: str = "json"):
    try :
        df = retrive_watchlist_from_user(username)
        if df.empty:
            raise HTTPException(status_code=404, detail=f"User '{username}' has an empty watchlist")
        if format == "csv":
            return StreamingResponse(
                io.StringIO(df.to_csv(index=False)),
                media_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename=watchlist-{username}.csv"}
            )
        return df.to_dict(orient="records")  # default JSON
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=404, detail=f'User {username} not found')

@router.post("/intersect")
def intersect_watchlist(users: List[str] = Body(
    ...,
    description="List of Letterboxd usernames to intersect", 
    example=["username1", "username2"])):
    try:
        watchlists = []
        for u in users:
            df = retrive_watchlist_from_user(u)
            if df.empty:
                raise HTTPException(status_code=404, detail=f"User '{u}' not found or empty watchlist")
            watchlists.append(df)
        results = intersect_watchlists(watchlists)
        if results.empty:
            raise HTTPException(status_code=404, detail='No movies in common')
        return results.to_dict(orient='records')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

