import 'package:flutter/material.dart';
import 'dart:convert'; // For JSON encoding
import 'package:http/http.dart' as http;
import 'package:shieldbot/bruteforce/presentation/attackstatus.dart';
import 'package:shieldbot/keys.dart';

class BruteforceScreen extends StatefulWidget {
  const BruteforceScreen({super.key});

  @override
  State<BruteforceScreen> createState() => _BruteforceScreenState();
}

class _BruteforceScreenState extends State<BruteforceScreen> {
  bool performbruteforce = false;
  bool performsqlinjection = false;
  bool performdos = false;
  final TextEditingController baseUrlController = TextEditingController();
  final TextEditingController dosrequestcountController =
      TextEditingController();
  var base_url;
  var sqlinjection_payload = [];
  var dos_request_count = 0;

  Future<void> Startattack() async {
    final url = Uri.parse('http://$backend_url/test-website');
    final body = {
      "base_url": base_url,
      "options": {
        "brute_force": {
          "passwords": ["admin", "password123"]
        },
        "sql_injection": {"payloads": sqlinjection_payload},
        "dos": {"request_count": dos_request_count}
      }
    };
    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(body),
      );

      if (response.statusCode == 202) {
        final jsonResponse = jsonDecode(response.body);
        final message = jsonResponse['message'];
        final taskId = jsonResponse['task_id'];
        print('Response: ${response.body}');
        showDialog(
          context: context,
          builder: (BuildContext context) {
            return AlertDialog(
              title: Text('Response'),
              content: Text('Message: $message\nTask ID: $taskId'),
              actions: [
                TextButton(
                  onPressed: () {
                    Navigator.of(context).pop();
                  },
                  child: Text('Perform New Attack'),
                ),
                TextButton(
                  onPressed: () {
                    Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => AttackStatusScreen(
                            taskId: taskId,
                          ),
                        ));
                  },
                  child: Text('Check Attack Status'),
                ),
              ],
            );
          },
        );
      } else {
        print('Error: ${response.statusCode}, ${response.body}');
      }
    } catch (e) {
      print('Failed to send POST request: $e');
    }
  }

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
                  Text(
                    'Check for Vulnerabilities',
                    style: TextStyle(fontSize: 25, fontWeight: FontWeight.w700),
                  ),
                  SizedBox(
                    height: 10,
                  ),
                  Container(
                    width: MediaQuery.of(context).size.width * 0.3,
                    child: TextField(
                      controller: baseUrlController,
                      decoration: InputDecoration(
                        labelText: 'base_url',
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.all(Radius.circular(10)),
                        ),
                      ),
                    ),
                  ),
                  SizedBox(
                    height: 8,
                  ),
                  Text(
                    'Select attack type',
                    style: TextStyle(fontSize: 20),
                  ),
                  SizedBox(
                    height: 8,
                  ),
                  Container(
                    width: 300,
                    child: CheckboxListTile(
                      value: performbruteforce,
                      onChanged: (bool? value) {
                        setState(() {
                          performbruteforce = value!;
                        });
                      },
                      title: Text('Brute Force Attack'),
                    ),
                  ),
                  Container(
                    width: 300,
                    child: CheckboxListTile(
                      value: performsqlinjection,
                      onChanged: (bool? value) {
                        setState(() {
                          performsqlinjection = value!;
                        });
                      },
                      title: Text('SQL Injection'),
                    ),
                  ),
                  Container(
                    width: 300,
                    child: CheckboxListTile(
                      value: performdos,
                      onChanged: (bool? value) {
                        setState(() {
                          performdos = value!;
                        });
                      },
                      title: Text('DOS (Denial of Service)'),
                    ),
                  ),
                  ElevatedButton(
                      onPressed: () async {
                        base_url = baseUrlController.text;

                        if (base_url == null || base_url.isEmpty) {
                          // Show missing Base URL dialog
                          showDialog(
                            context: context,
                            builder: (BuildContext context) {
                              return AlertDialog(
                                title: Text('Missing Base URL'),
                                content: Text(
                                    'Please enter the Base URL before starting the attack.'),
                                actions: [
                                  TextButton(
                                    onPressed: () {
                                      Navigator.of(context).pop();
                                    },
                                    child: Text('OK'),
                                  ),
                                ],
                              );
                            },
                          );
                          return; // Exit early
                        }

                        if (performsqlinjection) {
                          sqlinjection_payload = [
                            "' OR '1'='1",
                            "' UNION SELECT NULL--"
                          ];
                        }

                        if (performdos) {
                          await showDialog(
                            context: context,
                            builder: (BuildContext context) {
                              return AlertDialog(
                                title: Text('Set Request Amount'),
                                content: Column(
                                  mainAxisSize: MainAxisSize.min,
                                  children: [
                                    TextField(
                                      controller: dosrequestcountController,
                                      keyboardType: TextInputType.number,
                                      decoration: InputDecoration(
                                        labelText: 'Request Amount',
                                        border: OutlineInputBorder(),
                                      ),
                                    ),
                                    SizedBox(height: 10),
                                    Wrap(
                                      spacing: 10,
                                      children: [
                                        for (int value in [
                                          100,
                                          200,
                                          500,
                                          -100,
                                          -200,
                                          -500
                                        ])
                                          ElevatedButton(
                                            onPressed: () {
                                              int currentAmount = int.tryParse(
                                                      dosrequestcountController
                                                          .text) ??
                                                  0;
                                              currentAmount += value;
                                              dosrequestcountController.text =
                                                  currentAmount.toString();
                                            },
                                            child: Text(
                                              (value > 0 ? '+' : '') +
                                                  value.toString(),
                                              style: TextStyle(fontSize: 16),
                                            ),
                                          ),
                                      ],
                                    ),
                                  ],
                                ),
                                actions: [
                                  TextButton(
                                    onPressed: () {
                                      Navigator.of(context).pop();
                                    },
                                    child: Text('Cancel'),
                                  ),
                                  ElevatedButton(
                                    onPressed: () {
                                      int enteredAmount = int.tryParse(
                                              dosrequestcountController.text) ??
                                          0;
                                      dos_request_count = enteredAmount;
                                      Navigator.of(context).pop();
                                    },
                                    child: Text('OK'),
                                  ),
                                ],
                              );
                            },
                          );
                        }

                        if (!performbruteforce &&
                            !performsqlinjection &&
                            !performdos) {
                          // Show warning dialog if no attack type is selected
                          showDialog(
                            context: context,
                            builder: (context) => AlertDialog(
                              title: Text('Warning'),
                              content: Text(
                                  'Select at least 1 Attack type to proceed.'),
                              actions: [
                                TextButton(
                                  onPressed: () {
                                    Navigator.of(context).pop();
                                  },
                                  child: Text('OK'),
                                ),
                              ],
                            ),
                          );
                          return; // Exit early
                        }

                        // If all validations are satisfied, start the attack
                        await Startattack();
                        baseUrlController.clear();
                        dosrequestcountController.clear();
                      },
                      style: ButtonStyle(
                          foregroundColor: WidgetStatePropertyAll(Colors.white),
                          backgroundColor:
                              WidgetStatePropertyAll(Colors.green)),
                      child: Text('Check Now'))
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
