import 'package:flutter/material.dart';
import 'package:shieldbot/presentation/components/footer.dart';
import 'package:shieldbot/presentation/components/header.dart';
import 'package:shieldbot/presentation/components/styles.dart';

class Dashboard extends StatefulWidget {
  const Dashboard({super.key});

  @override
  State<Dashboard> createState() => _DashboardState();
}

class _DashboardState extends State<Dashboard> {
  int attacktype = 0;
  List<String> attackName = ['DDOS', 'Port Scan', 'Brute Force', 'IP Location'];
  List<String> attackDescription = [
    'A DDoS (Distributed Denial of Service) attack is a cyberattack where multiple compromised systems flood a target server with excessive traffic, causing it to slow down or crash. Attackers use botnets to generate overwhelming requests, making the service unavailable to legitimate users. Common types of DDoS attacks include volumetric attacks, protocol attacks, and application-layer attacks.',
    'Port scanning is a technique used to identify open ports and services running on a target system. It helps attackers or security professionals map network vulnerabilities by detecting active services. Common tools for port scanning include Nmap, which can reveal potential entry points for exploitation.',
    'Brute force attacks involve systematically trying all possible combinations of passwords or encryption keys to gain unauthorized access. This method is time-consuming but can be effective if weak passwords are used. To prevent brute force attacks, security measures like CAPTCHA, account lockouts, and multi-factor authentication are recommended.',
    'IP location tracking determines the geographical location of a device using its IP address. It helps identify a users country, city, and ISP but may not always be precise. Businesses use it for security, fraud prevention, and personalized content delivery.'
  ];

  @override
  Widget build(BuildContext context) {
    final _pageheight = MediaQuery.of(context).size.height;
    final _pagewidth = MediaQuery.of(context).size.width;

    return Scaffold(
      body: Container(
        padding: EdgeInsets.symmetric(horizontal: _pagewidth * 0.1),
        decoration: AppStyles.containerDecoration,
        child: SingleChildScrollView(
          child: Column(
            children: [
              Header(pageheight: _pageheight, pagewidth: _pagewidth),
              Container(
                height: _pageheight,
                child: Container(
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.all(Radius.circular(10)),
                  ),
                  padding: EdgeInsets.all(50),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      Row(
                        mainAxisSize: MainAxisSize.max,
                        mainAxisAlignment: MainAxisAlignment.end,
                        children: [
                          ElevatedButton(
                              onPressed: () {
                                showDialog(
                                  context: context,
                                  builder: (context) {
                                    int _attackType = 0;
                                    return StatefulBuilder(
                                      builder: (context, setDialogState) {
                                        return AlertDialog(
                                          insetPadding: EdgeInsets.zero,
                                          contentPadding: EdgeInsets.zero,
                                          titlePadding: EdgeInsets.zero,
                                          shape: RoundedRectangleBorder(
                                            borderRadius:
                                                BorderRadius.circular(10),
                                          ),
                                          content: Row(
                                            mainAxisSize: MainAxisSize.min,
                                            crossAxisAlignment:
                                                CrossAxisAlignment.center,
                                            children: [
                                              Container(
                                                  height: _pageheight * 0.6,
                                                  padding: EdgeInsets.symmetric(
                                                      horizontal: 30),
                                                  child: Column(
                                                    mainAxisAlignment:
                                                        MainAxisAlignment
                                                            .center,
                                                    children: [
                                                      Container(
                                                        width: _pagewidth * 0.3,
                                                        child: Row(
                                                          mainAxisAlignment:
                                                              MainAxisAlignment
                                                                  .spaceEvenly,
                                                          mainAxisSize:
                                                              MainAxisSize.max,
                                                          children: [
                                                            GestureDetector(
                                                              onTap: () {
                                                                _attackType = 0;
                                                                setDialogState(
                                                                    () {});
                                                              },
                                                              child: Container(
                                                                padding:
                                                                    EdgeInsets
                                                                        .all(
                                                                            10),
                                                                width:
                                                                    _pagewidth *
                                                                        0.3 /
                                                                        4,
                                                                decoration:
                                                                    BoxDecoration(
                                                                        borderRadius:
                                                                            BorderRadius
                                                                                .only(
                                                                          topLeft:
                                                                              Radius.circular(10),
                                                                          // bottomLeft: _attackType == 0
                                                                          //     ? Radius.circular(0)
                                                                          //     : Radius.circular(10),
                                                                        ),
                                                                        color: (_attackType ==
                                                                                0)
                                                                            ? Colors.blue
                                                                            : Colors.white),
                                                                child: Text(
                                                                  attackName[0],
                                                                  textAlign:
                                                                      TextAlign
                                                                          .center,
                                                                  style: TextStyle(
                                                                      color: (_attackType ==
                                                                              0)
                                                                          ? Colors
                                                                              .white
                                                                          : Colors
                                                                              .black),
                                                                ),
                                                              ),
                                                            ),
                                                            GestureDetector(
                                                              onTap: () {
                                                                _attackType = 1;
                                                                setDialogState(
                                                                    () {});
                                                              },
                                                              child: Container(
                                                                padding:
                                                                    EdgeInsets
                                                                        .all(
                                                                            10),
                                                                width:
                                                                    _pagewidth *
                                                                        0.3 /
                                                                        4,
                                                                decoration: BoxDecoration(
                                                                    color: (_attackType ==
                                                                            1)
                                                                        ? Colors
                                                                            .blue
                                                                        : Colors
                                                                            .white),
                                                                child: Text(
                                                                  attackName[1],
                                                                  textAlign:
                                                                      TextAlign
                                                                          .center,
                                                                  style: TextStyle(
                                                                      color: (_attackType ==
                                                                              1)
                                                                          ? Colors
                                                                              .white
                                                                          : Colors
                                                                              .black),
                                                                ),
                                                              ),
                                                            ),
                                                            GestureDetector(
                                                              onTap: () {
                                                                _attackType = 2;
                                                                setDialogState(
                                                                    () {});
                                                              },
                                                              child: Container(
                                                                padding:
                                                                    EdgeInsets
                                                                        .all(
                                                                            10),
                                                                width:
                                                                    _pagewidth *
                                                                        0.3 /
                                                                        4,
                                                                decoration: BoxDecoration(
                                                                    color: (_attackType ==
                                                                            2)
                                                                        ? Colors
                                                                            .blue
                                                                        : Colors
                                                                            .white),
                                                                child: Text(
                                                                  attackName[2],
                                                                  textAlign:
                                                                      TextAlign
                                                                          .center,
                                                                  style: TextStyle(
                                                                      color: (_attackType ==
                                                                              2)
                                                                          ? Colors
                                                                              .white
                                                                          : Colors
                                                                              .black),
                                                                ),
                                                              ),
                                                            ),
                                                            GestureDetector(
                                                              onTap: () {
                                                                _attackType = 3;
                                                                setDialogState(
                                                                    () {});
                                                              },
                                                              child: Container(
                                                                padding:
                                                                    EdgeInsets
                                                                        .all(
                                                                            10),
                                                                width:
                                                                    _pagewidth *
                                                                        0.3 /
                                                                        4,
                                                                decoration:
                                                                    BoxDecoration(
                                                                        borderRadius:
                                                                            BorderRadius
                                                                                .only(
                                                                          topRight:
                                                                              Radius.circular(10),
                                                                          // bottomRight: _attackType == 0
                                                                          //     ? Radius.circular(10)
                                                                          //     : Radius.circular(0),
                                                                        ),
                                                                        color: (_attackType ==
                                                                                3)
                                                                            ? Colors.blue
                                                                            : Colors.white),
                                                                child: Text(
                                                                  attackName[3],
                                                                  textAlign:
                                                                      TextAlign
                                                                          .center,
                                                                  style: TextStyle(
                                                                      color: (_attackType ==
                                                                              3)
                                                                          ? Colors
                                                                              .white
                                                                          : Colors
                                                                              .black),
                                                                ),
                                                              ),
                                                            ),
                                                          ],
                                                        ),
                                                      ),
                                                      Container(
                                                          decoration: BoxDecoration(
                                                              borderRadius: BorderRadius.only(
                                                                  bottomLeft: Radius
                                                                      .circular(
                                                                          10),
                                                                  bottomRight: Radius
                                                                      .circular(
                                                                          10)),
                                                              color:
                                                                  Colors.blue),
                                                          padding:
                                                              EdgeInsets.all(
                                                                  10),
                                                          height:
                                                              _pageheight * 0.4,
                                                          width:
                                                              _pagewidth * 0.3,
                                                          child: _getMenu(
                                                              _attackType))
                                                    ],
                                                  )),
                                              Container(
                                                height: _pageheight * 0.6,
                                                padding: EdgeInsets.all(20),
                                                decoration: BoxDecoration(
                                                    borderRadius:
                                                        BorderRadius.only(
                                                            topRight: Radius
                                                                .circular(10),
                                                            bottomRight:
                                                                Radius.circular(
                                                                    10)),
                                                    color: Colors.blue),
                                                child: Column(
                                                  mainAxisSize:
                                                      MainAxisSize.min,
                                                  mainAxisAlignment:
                                                      MainAxisAlignment.center,
                                                  crossAxisAlignment:
                                                      CrossAxisAlignment.start,
                                                  children: [
                                                    Text(
                                                      attackName[_attackType],
                                                      style: AppStyles
                                                          .headingStyle
                                                          .copyWith(
                                                              color:
                                                                  Colors.white,
                                                              fontWeight:
                                                                  FontWeight
                                                                      .bold),
                                                      textAlign:
                                                          TextAlign.start,
                                                    ),
                                                    Container(
                                                      width: _pagewidth * 0.2,
                                                      child: Text(
                                                        attackDescription[
                                                            _attackType],
                                                        style: AppStyles
                                                            .bodyStyle
                                                            .copyWith(
                                                                fontSize: 16,
                                                                color: Colors
                                                                    .white70),
                                                        textAlign:
                                                            TextAlign.justify,
                                                        maxLines: 15,
                                                        overflow: TextOverflow
                                                            .ellipsis,
                                                      ),
                                                    )
                                                  ],
                                                ),
                                              )
                                            ],
                                          ),
                                        );
                                      },
                                    );
                                  },
                                );
                              },
                              child: Text('New Attack'))
                        ],
                      ),
                      Container(
                        height: _pageheight * 0.8,
                        decoration: BoxDecoration(
                          color: Colors.cyan,
                          borderRadius: BorderRadius.all(Radius.circular(10)),
                        ),
                        padding: EdgeInsets.all(50),
                        child: Container(
                          decoration: BoxDecoration(
                            color: const Color.fromARGB(255, 238, 216, 216),
                            borderRadius: BorderRadius.all(Radius.circular(10)),
                          ),
                          child: Row(
                            mainAxisSize: MainAxisSize.max,
                            crossAxisAlignment: CrossAxisAlignment.start,
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              _recentTasks(pagewidth: _pagewidth),
                              _taskStatus(pagewidth: _pagewidth),
                            ],
                          ),
                        ),
                      )
                    ],
                  ),
                ),
              ),
              Footer()
            ],
          ),
        ),
      ),
    );
  }
}

Widget _getMenu(int _attackType) {
  if (_attackType == 0) {
    return _ddosMenu();
  } else if (_attackType == 1) {
    return _portScanMenu();
  } else if (_attackType == 2) {
    return _bruteForceMenu();
  } else if (_attackType == 3) {
    return _ipLocationMenu();
  } else {
    return Container();
  }
}

class _ddosMenu extends StatelessWidget {
  const _ddosMenu({super.key});

  @override
  Widget build(BuildContext context) {
    return _buildContainer(
      children: [
        _styledTextField(
            label: 'Target URL', hint: 'ex: https://www.example.com'),
        _styledTextField(label: 'Worker Thread Count', hint: 'ex: 1 - 50'),
        _styledTextField(label: 'Attack Per Thread', hint: 'ex: 100,200'),
        _styledButton(label: 'Perform DDOS', onPressed: () {}),
      ],
    );
  }
}

class _portScanMenu extends StatelessWidget {
  const _portScanMenu({super.key});

  @override
  Widget build(BuildContext context) {
    return _buildContainer(
      children: [
        _styledTextField(label: 'Target URL', hint: 'ex: example.com'),
        _styledButton(label: 'Start Scan', onPressed: () {}),
      ],
    );
  }
}

class _bruteForceMenu extends StatelessWidget {
  const _bruteForceMenu({super.key});

  @override
  Widget build(BuildContext context) {
    final bruteForceOptions = ['Type 1', 'Type 2', 'Type 3'];

    return _buildContainer(
      children: [
        _styledTextField(
            label: 'Target URL', hint: 'https://www.example.com/login'),
        _styledDropdown(
          label: 'Select Attack Type',
          items: bruteForceOptions,
          onChanged: (value) => print("Selected attack type: $value"),
        ),
        _styledButton(label: 'Start Attack', onPressed: () {}),
      ],
    );
  }
}

class _ipLocationMenu extends StatelessWidget {
  const _ipLocationMenu({super.key});

  @override
  Widget build(BuildContext context) {
    return _buildContainer(
      children: [
        _styledTextField(label: 'Target IP Address', hint: '127.0.0.1'),
        _styledButton(label: 'Search Location', onPressed: () {}),
      ],
    );
  }
}

Widget _buildContainer({required List<Widget> children}) {
  return Container(
    padding: EdgeInsets.all(16),
    decoration: BoxDecoration(
      color: const Color.fromARGB(255, 80, 103, 103)
          .withOpacity(0.8), // Dark theme background
      borderRadius: BorderRadius.circular(12),
      boxShadow: [BoxShadow(color: Colors.black26, blurRadius: 8)],
    ),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        ...children.map((child) => Padding(
              padding: const EdgeInsets.only(bottom: 12),
              child: child,
            )),
      ],
    ),
  );
}

/// Creates a **stylized text field**.
Widget _styledTextField({required String label, required String hint}) {
  return TextField(
    style: TextStyle(color: Colors.white),
    decoration: InputDecoration(
      labelText: label,
      labelStyle: TextStyle(color: Colors.white, fontSize: 16),
      hintText: hint,
      hintStyle: TextStyle(color: Colors.white70, fontSize: 14),
      filled: true,
      fillColor: Colors.white.withOpacity(0.1),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: BorderSide(color: Colors.white, width: 1.5),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: BorderSide(color: Colors.blueAccent, width: 2),
      ),
      contentPadding: EdgeInsets.symmetric(vertical: 14, horizontal: 16),
    ),
    cursorColor: Colors.white,
  );
}

/// Creates a **stylized dropdown**.
Widget _styledDropdown({
  required String label,
  required List<String> items,
  required Function(String?) onChanged,
}) {
  return DropdownButtonFormField<String>(
    decoration: InputDecoration(
      labelText: label,
      labelStyle: TextStyle(color: Colors.white, fontSize: 16),
      filled: true,
      fillColor: Colors.white.withOpacity(0.1),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: BorderSide(color: Colors.white, width: 1.5),
      ),
      contentPadding: EdgeInsets.symmetric(vertical: 12, horizontal: 16),
    ),
    dropdownColor: Colors.black87,
    style: TextStyle(color: Colors.white),
    items: items.map((option) {
      return DropdownMenuItem<String>(
        value: option,
        child: Text(option, style: TextStyle(color: Colors.white)),
      );
    }).toList(),
    onChanged: onChanged,
  );
}

Widget _styledButton({required String label, required VoidCallback onPressed}) {
  return ElevatedButton(
    onPressed: onPressed,
    style: ElevatedButton.styleFrom(
      backgroundColor: Colors.blueAccent,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      padding: EdgeInsets.symmetric(vertical: 14),
      textStyle: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
    ),
    child: Text(label, style: TextStyle(color: Colors.white)),
  );
}

class _taskStatus extends StatelessWidget {
  const _taskStatus({
    super.key,
    required double pagewidth,
  }) : _pagewidth = pagewidth;

  final double _pagewidth;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(10),
      width: _pagewidth * 0.45,
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.all(Radius.circular(10)),
      ),
      child: Column(
        children: [
          Text(
            'Attack Status',
            style: AppStyles.headingStyle,
          ),
        ],
      ),
    );
  }
}

class _recentTasks extends StatelessWidget {
  const _recentTasks({
    super.key,
    required double pagewidth,
  }) : _pagewidth = pagewidth;

  final double _pagewidth;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(10),
      width: _pagewidth * 0.2,
      decoration: BoxDecoration(
        color: const Color.fromARGB(255, 238, 216, 216),
        borderRadius: BorderRadius.all(Radius.circular(10)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                'Recent Tasks',
                style: AppStyles.headingStyle,
              ),
            ],
          ),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'taskid - 1232 bruteforce',
                textAlign: TextAlign.start,
              ),
              Text('taskid - 1232 bruteforce'),
              Text('taskid - 1232 bruteforce'),
              Text('taskid - 1232 bruteforce'),
              Text('taskid - 1232 bruteforce'),
              Text('taskid - 1232 bruteforce'),
              Text('taskid - 1232 bruteforce')
            ],
          )
        ],
      ),
    );
  }
}
