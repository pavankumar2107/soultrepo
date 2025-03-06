import dao.user_dao as user_dao
import dao.financial_asset_dao as financial_asset_dao
import dao.non_material_memory_dao as non_material_asset_dao
import dao.security_questions_dao as security_questions_dao
import dao.end_life_preference_dao as end_life_preferences_dao
import dao.organ_donation_preferences_dao as organ_donation_preference_dao
from dao import loved_ones_dao

# USER
def find_user(user_id: str):
    return user_dao.find(user_id)

def update_user(user_id: str, updated_data: dict):
    return user_dao.update(user_id, updated_data)

# user_id is used a dummy parameter to handle for audit log
def create_user(user_id: str, user: dict):
    return user_dao.create(user_id, user)

# use_id is used a dummy parameter to handle for audit log
def delete_user(user_id: str, model_id: str):
    return user_dao.delete(user_id, model_id)

def find_phone(phone_number: str):
    return user_dao.find_phone(phone_number)

def find_email(email: str):
    return user_dao.find_email(email)


# Organ Donation Preference
def create_organ_donation_preference(user_id: str, organ_donation_preference: dict):
    return organ_donation_preference_dao.create(user_id, organ_donation_preference)


def update_organ_donation_preference(user_id: str, organ_donation_preference_id: str, updated_data: dict):
    return organ_donation_preference_dao.update(user_id, organ_donation_preference_id, updated_data)


def delete_organ_donation_preference(user_id: str, organ_donation_preference_id: str):
    return organ_donation_preference_dao.delete(user_id, organ_donation_preference_id)


def find_organ_donation_preference(user_id: str, organ_donation_preference_id: str):
    return organ_donation_preference_dao.find(user_id, organ_donation_preference_id)


def find_all_organ_donation_preferences(user_id: str):
    return organ_donation_preference_dao.find_all(user_id)


# Financial_Asset
def create_financial_asset(user_id: str, asset_data: dict):
    return financial_asset_dao.create(user_id, asset_data)


def update_financial_asset(user_id: str, asset_id: str, updated_data: dict):
    return financial_asset_dao.update(user_id, asset_id, updated_data)


def delete_financial_asset(user_id: str, asset_id: str):
    return financial_asset_dao.delete(user_id, asset_id)


def find_financial_asset(user_id: str, asset_id: str):
    return financial_asset_dao.find(user_id, asset_id)


def find_all_financial_asset(user_id: str):
    return financial_asset_dao.find_all(user_id)


# Loved Ones
def create_loved_ones(user_id: str, loved_ones_data: dict):
    return loved_ones_dao.create(user_id, loved_ones_data)


def delete_loved_ones(user_id: str, loved_one_id: str):
    return loved_ones_dao.delete(user_id, loved_one_id)


def update_loved_ones(user_id: str, loved_ones_id: str, updated_data: dict):
    return loved_ones_dao.update(user_id, loved_ones_id, updated_data)


def find_loved_ones(user_id: str, loved_ones_id: str):
    return loved_ones_dao.find(user_id, loved_ones_id)


def find_all_loved_ones(user_id: str):
    return loved_ones_dao.find_all(user_id)


# Non-material memory
def create_non_material_memory(user_id: str, non_material_asset_data: dict):
    return non_material_asset_dao.create(user_id, non_material_asset_data)


def update_non_material_memory(user_id: str, non_asset_id: str, updated_data: dict):
    return non_material_asset_dao.update(user_id, non_asset_id, updated_data)


def delete_non_material_memory(user_id: str, non_asset_id: str):
    return non_material_asset_dao.delete(user_id, non_asset_id)


def find_non_material_memory(user_id: str, asset_id: str):
    return non_material_asset_dao.find(user_id, asset_id)


def find_all_non_material_memory(user_id: str):
    return non_material_asset_dao.find_all(user_id)


# Security questions
def create_security_question(user_id: str, security_question: list):
    return security_questions_dao.create(user_id, security_question)


def validate_security_question(user_id: str, question_answer: dict):
    return security_questions_dao.validate(user_id, question_answer)


# End Life Preferences
def create_end_life_preferences(user_id: str, end_life_preferences: dict):
    return end_life_preferences_dao.create(user_id, end_life_preferences)


def delete_end_life_preferences(user_id: str, end_life_preferences_id: str):
    return end_life_preferences_dao.delete(user_id, end_life_preferences_id)


def update_end_life_preferences(user_id: str,  updated_data: dict):
    return end_life_preferences_dao.update(user_id, updated_data)


def find_end_life_preferences(user_id: str):
    return end_life_preferences_dao.find(user_id)
