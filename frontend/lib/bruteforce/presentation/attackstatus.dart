import 'package:flutter/material.dart';
import 'dart:convert'; // For JSON encoding
import 'package:http/http.dart' as http;

class AttackStatusScreen extends StatefulWidget {
  final String taskId;
  const AttackStatusScreen({super.key, required this.taskId});

  @override
  State<AttackStatusScreen> createState() => _AttackStatusScreenState();
}

class _AttackStatusScreenState extends State<AttackStatusScreen> {
  @override
  Widget build(BuildContext context) {
    final height = MediaQuery.of(context).size.height;
    final width = MediaQuery.of(context).size.width;
    return Scaffold(
      backgroundColor: const Color.fromARGB(255, 9, 13, 54),
      body: Center(
        child: Material(
          elevation: 10,
          borderRadius: BorderRadius.circular(25),
          child: Container(
            height: height * 0.8,
            width: width * 0.8,
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(25),
              color: const Color.fromARGB(255, 242, 242, 245),
            ),
            child: Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text('Attack Status here'),
                  Text('Task Started with Attack id '),
                  Text(widget.taskId)
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
