"""
数据验证器
"""

import re
from typing import Any, List, Optional
from dataclasses import dataclass


@dataclass
class ValidationError:
    """验证错误"""
    field: str
    message: str


class Validator:
    """数据验证器"""
    
    @staticmethod
    def required(value: Any, field: str = "field") -> Optional[ValidationError]:
        if value is None or value == "":
            return ValidationError(field, "不能为空")
        return None
    
    @staticmethod
    def min_length(value: str, min_len: int, field: str = "field") -> Optional[ValidationError]:
        if len(value) < min_len:
            return ValidationError(field, f"最小长度: {min_len}")
        return None
    
    @staticmethod
    def max_length(value: str, max_len: int, field: str = "field") -> Optional[ValidationError]:
        if len(value) > max_len:
            return ValidationError(field, f"最大长度: {max_len}")
        return None
    
    @staticmethod
    def email(value: str, field: str = "field") -> Optional[ValidationError]:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, value):
            return ValidationError(field, "邮箱格式无效")
        return None
    
    @staticmethod
    def url(value: str, field: str = "field") -> Optional[ValidationError]:
        pattern = r'^https?://[\w\.-]+\.\w+'
        if not re.match(pattern, value):
            return ValidationError(field, "URL 格式无效")
        return None
    
    @staticmethod
    def range(value: int, min_val: int, max_val: int, field: str = "field") -> Optional[ValidationError]:
        if not min_val <= value <= max_val:
            return ValidationError(field, f"范围: {min_val} - {max_val}")
        return None
    
    @staticmethod
    def pattern(value: str, pattern: str, field: str = "field") -> Optional[ValidationError]:
        if not re.match(pattern, value):
            return ValidationError(field, "格式不匹配")
        return None
    
    @staticmethod
    def validate(data: dict, rules: dict) -> List[ValidationError]:
        """批量验证"""
        errors = []
        for field, rule in rules.items():
            value = data.get(field)
            
            if "required" in rule and rule["required"]:
                error = Validator.required(value, field)
                if error:
                    errors.append(error)
                    continue
            
            if value is None:
                continue
            
            if "min_length" in rule:
                error = Validator.min_length(value, rule["min_length"], field)
                if error:
                    errors.append(error)
            
            if "max_length" in rule:
                error = Validator.max_length(value, rule["max_length"], field)
                if error:
                    errors.append(error)
            
            if "email" in rule and rule["email"]:
                error = Validator.email(value, field)
                if error:
                    errors.append(error)
            
            if "range" in rule:
                error = Validator.range(value, rule["range"][0], rule["range"][1], field)
                if error:
                    errors.append(error)
        
        return errors
