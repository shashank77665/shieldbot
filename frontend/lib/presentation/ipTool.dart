import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:shieldbot/functions/dns/dns.dart';
import 'package:shieldbot/presentation/components/footer.dart';
import 'package:shieldbot/presentation/components/header.dart';
import 'package:shieldbot/presentation/components/styles.dart';

class ipToolPage extends StatefulWidget {
  const ipToolPage({super.key});

  @override
  State<ipToolPage> createState() => _ipToolPageState();
}

class _ipToolPageState extends State<ipToolPage> {
  final TextEditingController _domainController = TextEditingController();
  Map<String, dynamic>? _resultip;

  @override
  Widget build(BuildContext context) {
    final _pageheight = MediaQuery.of(context).size.height * 0.7;
    final _pagewidth = MediaQuery.of(context).size.width;
    return Scaffold(
      body: Container(
        padding: EdgeInsets.symmetric(horizontal: _pagewidth * 0.1),
        decoration: AppStyles.containerDecoration,
        child: SingleChildScrollView(
          child: Column(
            children: [
              Header(
                pageheight: _pageheight,
                pagewidth: _pagewidth,
              ),
              Container(
                height: _pageheight,
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    Text(
                      'Find IP',
                      style: AppStyles.subheadingStyle,
                    ),
                    Text(
                      'Tools to find ip address corresponding to a domain name',
                      style: AppStyles.bodyStyle,
                    ),
                    SizedBox(
                      width: _pagewidth * 0.18,
                      child: TextField(
                        controller: _domainController,
                        decoration: InputDecoration(
                          hintText: 'google.com',
                          labelText: 'Domain Name',
                          labelStyle: TextStyle(color: Colors.white),
                          hintStyle: TextStyle(color: Colors.grey.shade500),
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(8),
                            borderSide: BorderSide(color: Colors.grey.shade300),
                          ),
                          enabledBorder: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(8),
                            borderSide: BorderSide(color: Colors.grey.shade300),
                          ),
                          focusedBorder: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(8),
                            borderSide:
                                BorderSide(color: Colors.white, width: 2),
                          ),
                        ),
                        style: TextStyle(color: Colors.white),
                      ),
                    ),
                    ElevatedButton(
                      style: ButtonStyle(
                        padding: WidgetStatePropertyAll(EdgeInsets.all(20)),
                        backgroundColor: WidgetStatePropertyAll(Colors.white),
                        elevation: WidgetStatePropertyAll(10),
                        shape: WidgetStatePropertyAll(
                          RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(10)),
                        ),
                      ),
                      onPressed: () async {
                        _resultip = await resolveIP("shieldbot.me");
                        print(_resultip);
                        context.go('/dnsresult');
                      },
                      child: Text('Fetch',
                          style: AppStyles.bodyStyle
                              .copyWith(color: Colors.black)),
                    ),
                  ],
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
