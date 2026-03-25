#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JWT 认证模块 - FastAPI API 安全

功能：
1. JWT Token 生成与验证
2. 用户注册/登录 API
3. Token 刷新机制
4. 权限控制中间件
5. 密码加密 (bcrypt)
"""

import jwt
from datetime import datetime, timedelta
from functools import wraps
from typing import Optional, Dict, List
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr


# ==================== 配置 ====================

SECRET_KEY = "your-secret-key-change-in-production"  # 生产环境请修改！
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24  # 30 天
REFRESH_TOKEN_EXPIRE_DAYS = 90  # 90 天


# ==================== Pydantic Models ====================

class Token(BaseModel):
    """Token 响应模型"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserRegisterRequest(BaseModel):
    """用户注册请求模型"""
    username: str
    email: EmailStr
    password: str
    
    # 密码验证
    @property
    def validate_password(self) -> bool:
        if len(self.password) < 8:
            raise ValueError("密码长度至少 8 位")
        return True


class UserLoginRequest(BaseModel):
    """用户登录请求模型"""
    username: str
    password: str


class TokenData(BaseModel):
    """Token 数据模型"""
    user_id: Optional[int] = None
    username: Optional[str] = None
    role: Optional[str] = None


# ==================== OAuth2 配置 ====================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login",
    description="JWT Bearer Token"
)


# ==================== JWT 工具函数 ====================

def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌
    
    Args:
        data: 要编码的数据 (必须包含 user_id)
        expires_delta: 过期时间
        
    Returns:
        str: JWT Token
    """
    
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: Dict) -> str:
    """创建刷新令牌
    
    Args:
        data: 要编码的数据
        
    Returns:
        str: JWT Refresh Token
    """
    
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """验证 JWT Token
    
    Args:
        token: JWT Token
        
    Returns:
        TokenData: 解析后的用户数据
    """
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="认证失败",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        user_id: int = payload.get("user_id")
        username: str = payload.get("username")
        role: str = payload.get("role", "user")
        
        if user_id is None:
            raise credentials_exception
        
        token_type = payload.get("type")
        if token_type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的 Token 类型"
            )
            
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token 已过期",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise credentials_exception
    
    return TokenData(user_id=user_id, username=username, role=role)


def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    """获取当前登录用户
    
    Args:
        token: JWT Token
        
    Returns:
        TokenData: 用户数据
    """
    
    return verify_token(token)


# ==================== 权限控制装饰器 ====================

def require_role(required_roles: List[str]):
    """权限控制装饰器
    
    Args:
        required_roles: 需要的角色列表 (如：['admin', 'user'])
        
    Returns:
        Decorator: 权限检查装饰器
    """
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 获取当前用户
            current_user = await get_current_user()
            
            # 检查角色权限
            if current_user.role not in required_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="没有权限访问此资源"
                )
            
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator


# ==================== FastAPI 端点 ====================

from fastapi import APIRouter

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegisterRequest):
    """用户注册
    
    - **username**: 用户名 (唯一)
    - **email**: 邮箱地址
    - **password**: 密码 (至少 8 位)
    
    返回：访问令牌和刷新令牌
    """
    
    from database.db_manager import DatabaseManager
    
    db = DatabaseManager()
    
    try:
        # 创建用户
        result = db.create_user(
            username=user_data.username,
            email=str(user_data.email),
            password=user_data.password,
            role="user"
        )
        
        if result["status"] == "error":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["message"]
            )
        
        user_id = result["user_id"]
        
        # 生成 Token
        access_token = create_access_token(data={"user_id": user_id, "username": user_data.username})
        refresh_token = create_refresh_token(data={"user_id": user_id})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    finally:
        db.close()


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """用户登录
    
    - **username**: 用户名
    - **password**: 密码
    
    返回：访问令牌和刷新令牌
    """
    
    from database.db_manager import DatabaseManager
    
    db = DatabaseManager()
    
    try:
        # 验证用户
        result = db.authenticate(form_data.username, form_data.password)
        
        if result["status"] == "error":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=result["message"],
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_id = result["user_id"]
        username = result["username"]
        
        # 生成 Token
        access_token = create_access_token(data={"user_id": user_id, "username": username})
        refresh_token = create_refresh_token(data={"user_id": user_id})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    finally:
        db.close()


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token_str: str):
    """刷新访问令牌
    
    - **refresh_token**: 有效的刷新令牌
    
    返回：新的访问令牌和刷新令牌
    """
    
    try:
        # 验证刷新令牌
        payload = jwt.decode(refresh_token_str, SECRET_KEY, algorithms=[ALGORITHM])
        
        token_type = payload.get("type")
        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的 Token 类型"
            )
        
        user_id = payload.get("user_id")
        
        # 从数据库获取用户信息
        from database.db_manager import DatabaseManager
        
        db = DatabaseManager()
        try:
            cursor = db.conn.cursor()
            cursor.execute(
                "SELECT username FROM users WHERE id = ?",
                (user_id,)
            )
            
            row = cursor.fetchone()
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="用户不存在"
                )
            
            username = row[0]
        finally:
            db.close()
        
        # 生成新 Token
        access_token = create_access_token(data={"user_id": user_id, "username": username})
        new_refresh_token = create_refresh_token(data={"user_id": user_id})
        
        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="刷新令牌已过期，请重新登录"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的刷新令牌"
        )


@router.get("/me", response_model=Dict)
async def get_current_user_info(current_user: TokenData = Depends(get_current_user)):
    """获取当前用户信息
    
    需要认证：是
    
    返回：当前用户的详细信息
    """
    
    from database.db_manager import DatabaseManager
    
    db = DatabaseManager()
    
    try:
        cursor = db.conn.cursor()
        cursor.execute("""
            SELECT id, username, email, created_at, last_login, role 
            FROM users WHERE id = ?
        """, (current_user.user_id,))
        
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        return {
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "created_at": row[3].isoformat() if row[3] else None,
            "last_login": row[4].isoformat() if row[4] else None,
            "role": row[5]
        }
    
    finally:
        db.close()


@router.get("/preferences", response_model=Dict)
async def get_user_preferences(
    current_user: TokenData = Depends(get_current_user)
):
    """获取用户偏好
    
    需要认证：是
    
    返回：用户的个性化设置
    """
    
    from database.db_manager import DatabaseManager
    
    db = DatabaseManager()
    
    try:
        prefs = db.get_user_preferences(current_user.user_id)
        
        if "error" in prefs:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=prefs["message"]
            )
        
        return prefs
    
    finally:
        db.close()


@router.put("/preferences", response_model=Dict)
async def update_user_preferences(
    preferences: Dict,
    current_user: TokenData = Depends(get_current_user)
):
    """更新用户偏好
    
    需要认证：是
    
    参数：
    - **preferred_topics**: 偏好的主题列表
    - **favorite_characters**: 喜欢的人物列表
    - **reading_frequency**: 阅读频率 (daily/weekly/monthly)
    - **notification_enabled**: 是否启用通知
    """
    
    from database.db_manager import DatabaseManager
    
    db = DatabaseManager()
    
    try:
        result = db.update_user_preferences(current_user.user_id, preferences)
        
        if result["status"] == "error":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["message"]
            )
        
        return {"status": "success", "message": "偏好已更新"}
    
    finally:
        db.close()


@router.get("/bookmarks", response_model=List[Dict])
async def get_user_bookmarks(
    current_user: TokenData = Depends(get_current_user)
):
    """获取用户收藏列表
    
    需要认证：是
    
    返回：用户的收藏案例列表
    """
    
    from database.db_manager import DatabaseManager
    
    db = DatabaseManager()
    
    try:
        bookmarks = db.get_bookmarks(current_user.user_id)
        
        # 添加案例详情
        from scripts.hybrid_search_v3 import SmartHybridSearch
        
        rag = SmartHybridSearch()
        
        for bookmark in bookmarks:
            case_data = rag.case_db.get(bookmark['case_name'], {})
            bookmark['title'] = case_data.get('title', '')
            bookmark['year'] = case_data.get('year', '')
        
        return bookmarks
    
    finally:
        db.close()


@router.post("/bookmarks", response_model=Dict)
async def add_bookmark(
    case_name: str,
    notes: Optional[str] = None,
    current_user: TokenData = Depends(get_current_user)
):
    """添加收藏
    
    需要认证：是
    
    参数：
    - **case_name**: 案例名称
    - **notes**: 备注信息 (可选)
    """
    
    from database.db_manager import DatabaseManager
    
    db = DatabaseManager()
    
    try:
        result = db.add_bookmark(current_user.user_id, case_name, notes)
        
        if result["status"] == "error":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["message"]
            )
        
        return {"status": "success", "message": "收藏成功"}
    
    finally:
        db.close()


@router.delete("/bookmarks/{case_name}", response_model=Dict)
async def remove_bookmark(
    case_name: str,
    current_user: TokenData = Depends(get_current_user)
):
    """移除收藏
    
    需要认证：是
    
    参数：
    - **case_name**: 案例名称
    """
    
    from database.db_manager import DatabaseManager
    
    db = DatabaseManager()
    
    try:
        result = db.remove_bookmark(current_user.user_id, case_name)
        
        if result["status"] == "error":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["message"]
            )
        
        return {"status": "success", "message": "收藏已移除"}
    
    finally:
        db.close()


@router.get("/progress", response_model=Dict)
async def get_user_progress(
    current_user: TokenData = Depends(get_current_user)
):
    """获取用户学习进度
    
    需要认证：是
    
    返回：用户的阅读统计信息
    """
    
    from database.db_manager import DatabaseManager
    
    db = DatabaseManager()
    
    try:
        progress = db.get_user_progress(current_user.user_id)
        
        if "error" in progress:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=progress["message"]
            )
        
        return progress
    
    finally:
        db.close()


# ==================== 测试 ====================

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 80)
    print("🔐 JWT 认证模块测试")
    print("=" * 80)
    
    # 创建 FastAPI 应用
    from fastapi import FastAPI
    
    app = FastAPI(title="Auth Test API")
    
    # 注册路由
    app.include_router(router)
    
    print("\n✅ 认证模块已加载")
    print("📝 可用端点:")
    print("   POST /api/auth/register - 用户注册")
    print("   POST /api/auth/login - 用户登录")
    print("   POST /api/auth/refresh - 刷新 Token")
    print("   GET /api/auth/me - 获取当前用户信息")
    print("   GET /api/auth/preferences - 获取用户偏好")
    print("   PUT /api/auth/preferences - 更新用户偏好")
    print("   GET /api/auth/bookmarks - 获取收藏列表")
    print("   POST /api/auth/bookmarks - 添加收藏")
    print("   DELETE /api/auth/bookmarks/{case_name} - 移除收藏")
    
    # 启动测试服务器
    uvicorn.run(app, host="0.0.0.0", port=8001)
