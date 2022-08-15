from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import oauth2
from .. import models, schemas, utils, oauth2
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/user",
    tags=['users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.userOut)
def user_create(user: schemas.userCreate, db: Session = Depends(get_db)):
    '''user create(sign up)'''
    user_search_email = db.query(models.User).filter(
        models.User.email == user.email)
    user_search_phone = db.query(models.User).filter(
        models.User.phone_number == user.phone_number)
    if len(user.phone_number) < 10 or len(user.phone_number) > 10:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Invalid Phone Number')
    if user_search_email.first() or user_search_phone.first():
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='user exists')
    user.password = utils.hash_password(user.password)
    new_user = models.User(**user.dict())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{Exception},Error')
    return new_user


@router.post('/user_collect', status_code=status.HTTP_201_CREATED, response_model=schemas.userCollectOut)
def user_data_collect(user_data_payload: schemas.userCollect, db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    '''collect users data'''
    user_search_email = db.query(models.User_data).filter(
        models.User_data.email == user_data_payload.email)
    user_search_phone = db.query(models.User_data).filter(
        models.User_data.phone_number == user_data_payload.phone_number)
    if user_search_email.first() or user_search_phone.first():
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'user exists')
    user_data = models.User_data(
        owner_id=current_user.id, **user_data_payload.dict())
    try:
        db.add(user_data)
        db.commit()
        db.refresh(user_data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{Exception},Error')
    return user_data


@router.post('/user_location_data', status_code=status.HTTP_201_CREATED, response_model=schemas.user_location_data_out)
def user_location_data(user_location_data_payload: schemas.user_location_data_in, db: Session = Depends(get_db),
                       current_user: int = Depends(oauth2.get_current_user)):
    '''collection of user location data '''
    user_search = db.query(models.User_location_data).filter(
        models.User_location_data.owner_id == current_user.id)
    if user_search.first():
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'user exists')
    user_location_data_in = models.User_location_data(
        owner_id=current_user.id, **user_location_data_payload.dict())
    try:
        db.add(user_location_data_in)
        db.commit()
        db.refresh(user_location_data_in)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{Exception},Error')
    return user_location_data_in


@router.get('/user_out_phno/{ph_no}', response_model=schemas.user_data_out)
def get_user(ph_no: int, db: Session = Depends(get_db)):
    '''only for admin'''
    user_search = db.query(models.User).filter(
        models.User.phone_number == ph_no).first()
    if not user_search:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'user with {ph_no} does not exist')
    return user_search


@router.get('/user_out_dac/{dac}')
def get_user_dac(dac: str, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    '''get location data of user by 12-digit code'''
    dac_search = db.query(models.Digital_access_code).filter(
        models.Digital_access_code.digital_access_code == dac).first()
    if not dac_search:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'{dac} : Not found')
    location_data = db.query(models.User_location_data).filter(
        models.User_location_data.owner_id == dac_search.owner_id).first()
    full_data = {'dac_data': dac_search, 'location_data': location_data}
    return full_data
