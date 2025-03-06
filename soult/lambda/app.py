from fastapi import FastAPI
from mangum import Mangum
from router.user_router import router as user_router
from router.financial_asset_router import router as financial_asset_router
from router.non_material_memories_router import router as non_material_memories_router
from router.loved_ones_router import router as loved_ones_router
from router.security_question_router import router as security_question_router
from router.end_life_preference_router import router as end_life_preference_router
from router.organ_donation_preferences_router import router as organ_donation_preferences_router
from router.ses_router import router as ses_router

app = FastAPI()

app.include_router(user_router)
app.include_router(financial_asset_router)
app.include_router(non_material_memories_router)
app.include_router(loved_ones_router)
app.include_router(security_question_router)
app.include_router(end_life_preference_router)
app.include_router(organ_donation_preferences_router)
app.include_router(ses_router)

def lambda_handler(event, context):
    handler = Mangum(app)
    return handler(event, context)
