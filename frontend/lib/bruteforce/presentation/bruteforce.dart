import 'package:flutter/material.dart';

class BruteforceScreen extends StatefulWidget {
  const BruteforceScreen({super.key});

  @override
  State<BruteforceScreen> createState() => _BruteforceScreenState();
}

class _BruteforceScreenState extends State<BruteforceScreen> {
  bool performbruteforce = false;
  bool performsqlinjection = false;
  bool performdos = false;

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
                      onPressed: () {},
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
