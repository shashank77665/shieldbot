from flask import Blueprint, jsonify, redirect, url_for, request, session

main_bp = Blueprint("main", __name__)

@main_bp.route('/')
def home():
    """Simple homepage that lists available attacks"""
    available_attacks = [
        {"id": "ddos", "name": "DDoS Attack", "description": "Distributed Denial of Service attack using GoldenEye"},
        {"id": "port_scan", "name": "Port Scan", "description": "Scan target for open ports and services"},
        {"id": "ip_location", "name": "IP Location", "description": "Find geographical location of target IP address"},
        {"id": "brute_force", "name": "Brute Force", "description": "Password cracking and forum testing"}
    ]
    
    return jsonify({
        "message": "Welcome to ShieldBot API",
        "version": "1.0.0",
        "available_attacks": available_attacks,
        "documentation": "/docs",
        "login_required": True
    })

@main_bp.route('/docs')
def docs():
    """Simple API documentation"""
    endpoints = [
        {
            "path": "/",
            "method": "GET",
            "description": "Get available attacks"
        },
        {
            "path": "/attack/perform-test",
            "method": "POST",
            "description": "Start a new attack test",
            "auth_required": True,
            "body": {
                "base_url": "http://example.com",
                "attack_type": "port_scan|ddos|ip_location|brute_force",
                "options": {}
            }
        },
        {
            "path": "/attack/test-status/<test_id>",
            "method": "GET",
            "description": "Get status and logs for a test",
            "auth_required": True
        },
        {
            "path": "/attack/list-tests",
            "method": "GET",
            "description": "List all tests for the current user",
            "auth_required": True
        },
        {
            "path": "/auth/login",
            "method": "POST",
            "description": "Login with username/password",
            "body": {
                "username": "username",
                "password": "password"
            }
        },
        {
            "path": "/auth/signup",
            "method": "POST",
            "description": "Create a new account",
            "body": {
                "username": "username",
                "email": "email@example.com",
                "password": "password"
            }
        }
    ]
    
    return jsonify({
        "api_name": "ShieldBot API",
        "version": "1.0.0",
        "endpoints": endpoints
    }) 