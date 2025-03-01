import 'package:flutter/material.dart';

class AppStyles {
  static const Color neutral = Color(0xFF141516);
  static const Color success = Color(0xFF9ED23E);
  static const Color caution = Color(0xFFF1AE05);
  static const Color danger = Color(0xFFE45316);
  static const Color info = Color(0xFF048DD9);
  static const Color lightcolor = Color.fromARGB(255, 234, 229, 254);
  static const Color primaryBackground = Color.fromARGB(255, 15, 22, 41);
  static const Color secondaryBackground = Color.fromARGB(255, 15, 29, 41);

  static const TextStyle headingStyle = TextStyle(
    fontSize: 68,
    color: Colors.white,
    fontWeight: FontWeight.w600,
  );

  static const TextStyle subheadingStyle = TextStyle(
    fontSize: 40,
    color: Colors.white,
    fontWeight: FontWeight.w600,
  );

  static const TextStyle bodyStyle = TextStyle(
    fontSize: 18,
    color: Color.fromARGB(255, 225, 224, 233),
    fontWeight: FontWeight.w400,
  );

  static const BoxDecoration containerDecoration = BoxDecoration(
    gradient: LinearGradient(
      colors: [AppStyles.primaryBackground, AppStyles.secondaryBackground],
      begin: Alignment.topRight,
      end: Alignment.bottomLeft,
    ),
  );
}
