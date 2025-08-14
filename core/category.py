from utils.json_io import load_user_info, save_user_info

class CategoryManager:
    def __init__(self, user_id):
        self.user_id = user_id
        self.categories = self.load_categories()
    
    
    def load_categories(self):
        raw_user_data = load_user_info(self.user_id)
        if raw_user_data and "categories" in raw_user_data:
            return raw_user_data["categories"]
        else:
            raise ValueError(f"Categories not found for user {self.user_id}")
        
        
    def get_income_categories(self):
        return self.categories["income"]
    
    
    def get_expense_categories(self):
        return self.categories["expense"]
        
        
    def add_category(self, category_type, category_name):
        if category_name not in self.categories[category_type]:
            self.categories[category_type].append(category_name)
            save_user_info(self.user_id, self.categories)
            return True
        else:
            return False 
        
        
    def view_categories(self):
        return self.categories
    
    
        