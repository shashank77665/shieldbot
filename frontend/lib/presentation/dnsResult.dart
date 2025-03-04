import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:shieldbot/presentation/components/footer.dart';
import 'package:shieldbot/presentation/components/header.dart';
import 'package:shieldbot/presentation/components/styles.dart';

class IpResolveResultPage extends StatefulWidget {
  final Map<String, dynamic>? resultip;

  const IpResolveResultPage({super.key, required this.resultip});

  @override
  State<IpResolveResultPage> createState() => _IpResolveResultPageState();
}

class _IpResolveResultPageState extends State<IpResolveResultPage> {
  late final List<String> _parsedIPs;

  @override
  void initState() {
    super.initState();
    _parsedIPs = _extractIPs(widget.resultip);
  }

  List<String> _extractIPs(Map<String, dynamic>? resultip) {
    if (resultip == null || resultip['Answer'] == null) return [];
    return (resultip['Answer'] as List)
        .map((answer) => answer['data'].toString())
        .toList();
  }

  @override
  Widget build(BuildContext context) {
    final double pageHeight = MediaQuery.of(context).size.height * 0.7;
    final double pageWidth = MediaQuery.of(context).size.width;

    return Scaffold(
      body: Container(
        padding: EdgeInsets.symmetric(horizontal: pageWidth * 0.1),
        decoration: AppStyles.containerDecoration,
        child: SingleChildScrollView(
          child: Column(
            children: [
              Header(pageheight: pageHeight, pagewidth: pageWidth),
              SizedBox(height: 20),
              Container(
                height: pageHeight,
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    Text('Result', style: AppStyles.subheadingStyle),
                    Text(
                      'Tools to find IP address corresponding to a domain name',
                      style: AppStyles.bodyStyle,
                      textAlign: TextAlign.center,
                    ),
                    _parsedIPs.isNotEmpty
                        ? Column(
                            children: _parsedIPs
                                .map((ip) =>
                                    Text(ip, style: AppStyles.bodyStyle))
                                .toList(),
                          )
                        : Text('No data available', style: AppStyles.bodyStyle),
                    ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        padding: EdgeInsets.all(20),
                        backgroundColor: Colors.white,
                        elevation: 10,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(10),
                        ),
                      ),
                      onPressed: () {
                        context.go('/iptool');
                      },
                      child: Text(
                        'Search Again',
                        style:
                            AppStyles.bodyStyle.copyWith(color: Colors.black),
                      ),
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
