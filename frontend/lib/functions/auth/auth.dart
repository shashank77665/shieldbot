import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

Future<void> signUpUser(String username, String email, String password) async {
  const String url = "http://13.233.91.145/auth/signup";

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
    } else if (response.statusCode == 400) {
      print("User Already Exists");
    }
  } catch (e) {
    print("Error : $e");
  }
}

Future<void> logIn(String email, String password) async {
  const String url = "http://13.233.91.145/auth/login";

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

      final prefs = await SharedPreferences.getInstance();
      await prefs.setString("auth_token", token);

      print("Signin Sucessfull : ${response.body}");
    } else if (response.statusCode == 401) {
      print("Invalid email or password");
    }
  } catch (e) {
    print("Error : $e");
  }
}

Future<void> isTokenValid(String token) async {
  const String url = "http://13.233.91.145/auth/verify-token";

  try {
    final response = await http.post(
      Uri.parse(url),
      headers: {
        "Content-Type": "application/json",
      },
      body: jsonEncode({"Authorization": token}),
    );

    if (response.statusCode == 200) {
      print("Token is valid");
    } else if (response.statusCode == 400) {
      print("Token is missing");
    } else if (response.statusCode == 401) {
      print("Token is expired");
    }
  } catch (e) {
    print("Error : $e");
  }
}
