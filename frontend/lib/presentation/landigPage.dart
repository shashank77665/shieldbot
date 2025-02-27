import 'package:flutter/material.dart';
import 'package:shieldbot/presentation/components/footer.dart';
import 'package:shieldbot/presentation/components/header.dart';
import 'package:shieldbot/presentation/components/styles.dart';

class LandingPage extends StatelessWidget {
  const LandingPage({super.key});

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
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Header(),
              _welcomeWidget(
                pageheight: _pageheight,
                pagewidth: _pagewidth,
              ),
              Footer()
            ],
          ),
        ),
      ),
    );
  }
}

class _welcomeWidget extends StatelessWidget {
  const _welcomeWidget({
    required double pageheight,
    required double pagewidth,
  })  : _pageheight = pageheight,
        _pagewidth = pagewidth;

  final double _pageheight;
  final double _pagewidth;

  @override
  Widget build(BuildContext context) {
    return Container(
      height: _pageheight,
      width: double.infinity,
      child: Container(
        child: Row(
          mainAxisSize: MainAxisSize.max,
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Column(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'shieldBot',
                  style: TextStyle(
                    fontSize: 48,
                    fontWeight: FontWeight.w900,
                    color: const Color.fromARGB(255, 223, 111, 111),
                  ),
                ),
                Column(
                  mainAxisAlignment: MainAxisAlignment.start,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Test Security',
                      style: TextStyle(
                        fontSize: 60,
                        fontWeight: FontWeight.w500,
                        color: const Color.fromARGB(255, 132, 103, 101),
                      ),
                    ),
                    Text(
                      'Before Hackers Do!',
                      style: TextStyle(
                        fontSize: 60,
                        fontWeight: FontWeight.w500,
                        color: Colors.red,
                      ),
                    ),
                  ],
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  mainAxisSize: MainAxisSize.max,
                  children: [
                    ElevatedButton(
                        style: ButtonStyle(
                            padding:
                                WidgetStatePropertyAll(EdgeInsets.all(30))),
                        onPressed: () {},
                        child: Text('Check Now')),
                    SizedBox(
                      width: 60,
                    ),
                    ElevatedButton(
                        style: ButtonStyle(
                            padding:
                                WidgetStatePropertyAll(EdgeInsets.all(30))),
                        onPressed: () {},
                        child: Text('Browse Features'))
                  ],
                )
              ],
            ),
            Image.asset(
              "/Volumes/Data/Projects/shieldbot/frontend/assets/images/safety.png",
              width: _pagewidth * 0.3,
            )
          ],
        ),
      ),
    );
  }
}
