import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';
import 'package:shieldbot/bruteforce/presentation/bruteforce.dart';

class Home extends StatefulWidget {
  const Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  @override
  Widget build(BuildContext context) {
    final height = MediaQuery.of(context).size.height;
    final width = MediaQuery.of(context).size.width;
    return Scaffold(
        backgroundColor: const Color.fromARGB(255, 9, 13, 54),
        body: SingleChildScrollView(
          child: Column(
            children: [
              Container(
                padding: EdgeInsets.symmetric(vertical: 10),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    Row(
                      children: [
                        Text(
                          'shieldBot',
                          style: TextStyle(
                              fontSize: 30,
                              fontWeight: FontWeight.w800,
                              color: Colors.white),
                        )
                      ],
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          'Home',
                          style: TextStyle(
                              fontSize: 25,
                              fontWeight: FontWeight.w400,
                              color: Colors.white),
                        ),
                        SizedBox(
                          width: 12,
                        ),
                        Text(
                          'Company',
                          style: TextStyle(
                              fontSize: 25,
                              fontWeight: FontWeight.w400,
                              color: Colors.white),
                        ),
                        SizedBox(
                          width: 12,
                        ),
                        Text(
                          'Contact',
                          style: TextStyle(
                              fontSize: 25,
                              fontWeight: FontWeight.w400,
                              color: Colors.white),
                        ),
                        SizedBox(
                          width: 12,
                        ),
                        Text(
                          'Services',
                          style: TextStyle(
                              fontSize: 25,
                              fontWeight: FontWeight.w400,
                              color: Colors.white),
                        ),
                        SizedBox(
                          width: 12,
                        ),
                        Text(
                          'Blog',
                          style: TextStyle(
                              fontSize: 25,
                              fontWeight: FontWeight.w400,
                              color: Colors.white),
                        ),
                      ],
                    )
                  ],
                ),
              ),
              Center(
                child: Container(
                  padding: EdgeInsets.symmetric(horizontal: 100),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.start,
                    children: [
                      Container(
                        width: 500,
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Industry Specific & Powerful Reports',
                              style: TextStyle(
                                  fontSize: 25,
                                  color: Colors.white,
                                  fontWeight: FontWeight.w700),
                            ),
                            SizedBox(
                              height: 10,
                            ),
                            Text(
                              'Different industries require different needs. Our team has experience working in Healthcare, Financial Services, Legal, and with Software Companies.',
                              style: TextStyle(
                                  fontSize: 20,
                                  color: Colors.white,
                                  fontWeight: FontWeight.w400),
                            ),
                            SizedBox(
                              height: 10,
                            ),
                            Row(
                              children: [
                                Icon(
                                  Icons.import_contacts,
                                  color: Colors.red,
                                ),
                                SizedBox(
                                  width: 10,
                                ),
                                Text(
                                  'Maintain',
                                  style: TextStyle(
                                      fontSize: 20,
                                      color: Colors.white,
                                      fontWeight: FontWeight.w400),
                                )
                              ],
                            ),
                            Row(
                              children: [
                                Icon(
                                  Icons.import_contacts,
                                  color: Colors.red,
                                ),
                                SizedBox(
                                  width: 10,
                                ),
                                Text(
                                  'Maintain',
                                  style: TextStyle(
                                      fontSize: 20,
                                      color: Colors.white,
                                      fontWeight: FontWeight.w400),
                                )
                              ],
                            ),
                            Row(
                              children: [
                                Icon(
                                  Icons.import_contacts,
                                  color: Colors.red,
                                ),
                                SizedBox(
                                  width: 10,
                                ),
                                Text(
                                  'Maintain',
                                  style: TextStyle(
                                      fontSize: 20,
                                      color: Colors.white,
                                      fontWeight: FontWeight.w400),
                                )
                              ],
                            ),
                            SizedBox(
                              height: 10,
                            ),
                            ElevatedButton(
                                onPressed: () => Navigator.push(
                                    context,
                                    MaterialPageRoute(
                                      builder: (context) => BruteforceScreen(),
                                    )),
                                child: Text('Start Scan'))
                          ],
                        ),
                      ),
                      SvgPicture.asset(
                        'assets/images/widgets_dark.svg',
                      ),
                    ],
                  ),
                ),
              ),
              Container(
                width: double.infinity,
                padding:
                    const EdgeInsets.symmetric(vertical: 50, horizontal: 30),
                color: Colors.black,
                child: Row(
                  mainAxisSize: MainAxisSize.max,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'shieldBot',
                          style: TextStyle(
                            fontSize: 25,
                            fontWeight: FontWeight.w800,
                            color: Colors.white,
                          ),
                        ),
                        SizedBox(
                          height: 10,
                        ),
                        Container(
                          width: 500,
                          child: const Text(
                            'We are a cybersecurity technology platform that has sourced the tools, methods, and techniques attackers use. Our system allows owners and operators to find potential risks and exposures before attackers do.',
                            textAlign: TextAlign.start,
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.w400,
                              color: Colors.white,
                            ),
                          ),
                        ),
                        const SizedBox(height: 20),
                        Container(
                          width: 300,
                          child: const Text(
                            'By conducting scans you agree to our Terms',
                            textAlign: TextAlign.start,
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.w400,
                              color: Colors.white,
                            ),
                          ),
                        ),
                        const SizedBox(height: 20),
                        Container(
                          width: 300,
                          child: const Text(
                            'Copyright by shieldBot, LLC\n2025, All Rights Reserved.',
                            textAlign: TextAlign.start,
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.w400,
                              color: Colors.white,
                            ),
                          ),
                        ),
                      ],
                    ),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      spacing: 10,
                      children: [
                        Text(
                          'Useful Links',
                          style: TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.w800,
                            color: Colors.white,
                          ),
                        ),
                        TextButton(
                          onPressed: () {},
                          child: const Text(
                            'Home',
                            style: TextStyle(
                              fontSize: 20,
                              fontWeight: FontWeight.w400,
                              color: Colors.white,
                            ),
                          ),
                        ),
                        TextButton(
                          onPressed: () {},
                          child: const Text(
                            'Company',
                            style: TextStyle(
                              fontSize: 20,
                              fontWeight: FontWeight.w400,
                              color: Colors.white,
                            ),
                          ),
                        ),
                        TextButton(
                          onPressed: () {},
                          child: const Text(
                            'Services',
                            style: TextStyle(
                              fontSize: 20,
                              fontWeight: FontWeight.w400,
                              color: Colors.white,
                            ),
                          ),
                        ),
                        TextButton(
                          onPressed: () {},
                          child: const Text(
                            'Contact Us',
                            style: TextStyle(
                              fontSize: 20,
                              fontWeight: FontWeight.w400,
                              color: Colors.white,
                            ),
                          ),
                        ),
                      ],
                    ),
                    Column(
                      mainAxisAlignment: MainAxisAlignment.start,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      spacing: 10,
                      children: [
                        Text(
                          'Terms',
                          style: TextStyle(
                            fontSize: 25,
                            fontWeight: FontWeight.w800,
                            color: Colors.white,
                          ),
                        ),
                        TextButton(
                          onPressed: () {},
                          child: const Text(
                            'Privacy Policy',
                            style: TextStyle(
                              fontSize: 20,
                              fontWeight: FontWeight.w400,
                              color: Colors.white,
                            ),
                          ),
                        ),
                        TextButton(
                          onPressed: () {},
                          child: const Text(
                            'Terms & Conditions',
                            style: TextStyle(
                              fontSize: 20,
                              fontWeight: FontWeight.w400,
                              color: Colors.white,
                            ),
                          ),
                        ),
                      ],
                    ),
                    Column(
                      children: [
                        Text(
                          'Contact US',
                          style: TextStyle(
                            fontSize: 25,
                            fontWeight: FontWeight.w800,
                            color: Colors.white,
                          ),
                        ),
                        const Text(
                          'contact@shieldBot.com\n20283 State Road 7, Suite 108\nBoca Raton, Florida\n33434',
                          textAlign: TextAlign.center,
                          style: TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.w400,
                            color: Colors.white,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              )
            ],
          ),
        ));
  }
}
