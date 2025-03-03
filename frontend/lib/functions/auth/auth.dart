import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:go_router/go_router.dart';
import 'package:shared_preferences/shared_preferences.dart';

String backed_url = "https://backend.shieldbot.me";

Future<String> signUpUser(
    String username, String email, String password) async {
  String url = "$backed_url/auth/signup";

  try {
    final response = await http.post(
      Uri.parse(url),
      headers: {
        "Content-Type": "application/json",
      },
      body: jsonEncode({
        "username": username,
        "email": email,
        "password": password,
      }),
    );

    if (response.statusCode == 201) {
      print("Signup Sucessfull : ${response.body}");
      return "Account Created Sucessfully";
    } else if (response.statusCode == 400) {
      print("User Already Exists");
      return "User Already Exists";
    }
  } catch (e) {
    print("Error : $e");
    return "$e";
  }
  return "Something went Wrong !";
}

Future<String> logIn(
    BuildContext context, String email, String password) async {
  String url = "$backed_url/auth/login";
  print("trying to login");

  try {
    final response = await http.post(
      Uri.parse(url),
      headers: {
        "Content-Type": "application/json",
      },
      body: jsonEncode({
        "email": email,
        "password": password,
      }),
    );

    if (response.statusCode == 200) {
      final responseData = jsonDecode(response.body);
      final token = responseData["token"];
      final user_email = responseData["user"]["email"];

      final username = responseData["user"]["username"];
      //   final user_id = responseData["user"]["id"];

      final prefs = await SharedPreferences.getInstance();
      await prefs.setString("auth_token", token);
      await prefs.setString("user_email", user_email);
      await prefs.setString("username", username);
      //    await prefs.setInt("user_id", user_id);

      print("User Token : $token}");
      print("User Email : $user_email");
      print("User Username : $username");
      //  print("User Id : $user_id");

      context.go('/dashboard');

      print("Signin Sucessfull : ${response.body}");
      context.go('/dashboard');
      return "Login Sucessfull";
    } else if (response.statusCode == 401) {
      print("Invalid email or password");
      return "Invalid email or password";
    }
  } catch (e) {
    print("Error : $e");
    return "$e";
  }

  return "failed to login";
}

Future<void> logOut(BuildContext context) async {
  String url = "$backed_url/auth/logout";

  try {
    final response = await http.post(Uri.parse(url));

    if (response.statusCode == 200) {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString("auth_token", "");
      print("Logged out Sucessfully");
      context.go('/landing');
    } else {
      print("Failed to logout.Status Code: ${response.body}");
    }
  } catch (e) {
    print("Error : $e");
  }
}

Future<bool> isTokenValid(String token) async {
  String url = "$backed_url/auth/verify-token";

  try {
    print("checking token validity");
    final response = await http.get(
      Uri.parse(url),
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer $token",
      },
      //  body: jsonEncode({"Authorization": token}),
    );

    print("Response Status: ${response.statusCode}");
    print("Response Body: ${response.body}");

    if (response.statusCode == 200) {
      print("Token is valid");
      return true;
    } else if (response.statusCode == 400) {
      print("Token is missing");
    } else if (response.statusCode == 401) {
      print("Token is expired");
    }
  } catch (e) {
    print("Error : $e");
  }
  return false;
}
