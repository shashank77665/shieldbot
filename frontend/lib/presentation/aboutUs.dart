import 'package:flutter/material.dart';
import 'package:shieldbot/presentation/components/footer.dart';
import 'package:shieldbot/presentation/components/header.dart';
import 'package:shieldbot/presentation/components/styles.dart';

class AboutUsPage extends StatelessWidget {
  const AboutUsPage({super.key});

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
              Header(
                pageheight: _pageheight,
                pagewidth: _pagewidth,
              ),
              Container(
                height: _pageheight,
                child: Center(
                  child: Text('About Us Page Content'),
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
