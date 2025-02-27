import 'package:flutter/material.dart';

class AppStyles {
  static const TextStyle headingStyle = TextStyle(
    fontSize: 25,
    color: Colors.black,
    fontWeight: FontWeight.w400,
  );

  static const BoxDecoration containerDecoration = BoxDecoration(
    gradient: LinearGradient(
      colors: [
        Color.fromARGB(255, 181, 210, 214),
        Color.fromARGB(255, 147, 219, 199)
      ],
      begin: Alignment.topRight,
      end: Alignment.bottomLeft,
    ),
  );
}
