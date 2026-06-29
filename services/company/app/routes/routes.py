from fastapi import APIRouter,status
from app.schema.schema import Companycreate,Companyupdate
from app.service.service import create_company,get_company,all_get_companies,update_company,delete_company

router = APIRouter(
    prefix="/company",
    tags=["company"]
)


@router.post("/",status_code=status.HTTP_201_CREATED)
async def company_create_route(data:Companycreate):
    return await create_company(data)

@router.get("/")
async def company_get_all_data_route():
    return await all_get_companies()

@router.get("/{company_id}")
async def company_data_route(company_id:str):
    return await get_company(company_id)

@router.put("/{company_id}")
async def update_company_route(company_id:str,data:Companyupdate):
    return await update_company(company_id,data)

@router.delete("/{company_id}")
async def delete_company_data_route(company_id:str):
    return await delete_company(company_id)