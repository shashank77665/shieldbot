import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
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
              Header(
                pageheight: _pageheight,
                pagewidth: _pagewidth,
              ),
              _welcomeWidget(
                pageheight: _pageheight,
                pagewidth: _pagewidth,
              ),
              _questionWidget(pageheight: _pageheight, pagewidth: _pagewidth),
              _ourservicesWidget(
                  pageheight: _pageheight, pagewidth: _pagewidth),
              _locationWidget(pageheight: _pageheight, pagewidth: _pagewidth),
              Footer()
            ],
          ),
        ),
      ),
    );
  }
}

class _locationWidget extends StatelessWidget {
  const _locationWidget({
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
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                'Expert Support',
                style: AppStyles.subheadingStyle
                    .copyWith(fontWeight: FontWeight.bold),
              ),
              SizedBox(
                height: 20,
              ),
              Container(
                width: _pagewidth * 0.3,
                child: Text(
                  'Faulty phone battery? Slow laptop? We have in-house tech experts who can assist you.',
                  style: AppStyles.bodyStyle,
                ),
              ),
              SizedBox(
                height: 20,
              ),
              Text(
                'Visit us !',
                style: AppStyles.subheadingStyle
                    .copyWith(fontWeight: FontWeight.bold),
              ),
              SizedBox(
                height: 20,
              ),
              Text(
                'Our locations',
                style: AppStyles.subheadingStyle
                    .copyWith(fontWeight: FontWeight.bold),
              ),
              SizedBox(
                height: 20,
              ),
              Container(
                width: _pagewidth * 0.3,
                child: Text(
                  '123 Anywhere St. Any City, State, Any Country (123) 456 7890',
                  style: AppStyles.bodyStyle,
                ),
              )
            ],
          ),
          Container(
            height: _pageheight * 0.5,
            width: _pagewidth * 0.3,
            decoration: BoxDecoration(
                color: const Color.fromARGB(102, 171, 153, 153),
                borderRadius: BorderRadius.only(
                  topRight: Radius.circular(40),
                )),
            child: Icon(
              Icons.support_agent,
              color: Colors.green,
              size: 300,
            ),
          )
        ],
      ),
    );
  }
}

class _ourservicesWidget extends StatelessWidget {
  const _ourservicesWidget({
    required double pageheight,
    required double pagewidth,
  })  : _pageheight = pageheight,
        _pagewidth = pagewidth;

  final double _pageheight;
  final double _pagewidth;

  @override
  Widget build(BuildContext context) {
    return Container(
      height: _pageheight * 0.8,
      child: Column(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Text(
            'Our Services',
            style: AppStyles.headingStyle,
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              _productCard(pageheight: _pageheight, pagewidth: _pagewidth),
              _productCard(pageheight: _pageheight, pagewidth: _pagewidth),
              _productCard(pageheight: _pageheight, pagewidth: _pagewidth)
            ],
          ),
          ElevatedButton(
            style: ButtonStyle(
              padding: WidgetStatePropertyAll(EdgeInsets.all(30)),
              backgroundColor: WidgetStatePropertyAll(
                  const Color.fromARGB(116, 173, 157, 157)),
              elevation: WidgetStatePropertyAll(10),
              shape: WidgetStatePropertyAll(
                RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
              ),
            ),
            onPressed: () {},
            child: Text('See All',
                style: AppStyles.bodyStyle.copyWith(fontSize: 30)),
          ),
        ],
      ),
    );
  }
}

class _productCard extends StatelessWidget {
  const _productCard({
    required double pageheight,
    required double pagewidth,
  })  : _pageheight = pageheight,
        _pagewidth = pagewidth;

  final double _pageheight;
  final double _pagewidth;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(20),
      height: _pageheight * 0.45,
      width: _pagewidth * 0.2,
      decoration: BoxDecoration(
          color: const Color.fromARGB(255, 86, 107, 126),
          borderRadius: BorderRadius.only(
              topRight: Radius.circular(40), bottomLeft: Radius.circular(40))),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.image,
            size: 120,
          ),
          SizedBox(
            height: 10,
          ),
          Text(
            'DDoS Prevention',
            style: AppStyles.headingStyle
                .copyWith(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          SizedBox(
            height: 10,
          ),
          Text(
            'All about DDOS Prevention system . It is body that describe DDOS prevention system.',
            style: AppStyles.bodyStyle,
          )
        ],
      ),
    );
  }
}

class _questionWidget extends StatelessWidget {
  const _questionWidget({
    required double pageheight,
    required double pagewidth,
  })  : _pageheight = pageheight,
        _pagewidth = pagewidth;

  final double _pageheight;
  final double _pagewidth;

  @override
  Widget build(BuildContext context) {
    return Container(
      height: _pageheight * 0.7,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Center(
            child: Icon(
              Icons.question_mark,
              color: Colors.red,
              size: 400,
            ),
          ),
          Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'What we do?',
                style: AppStyles.subheadingStyle,
              ),
              SizedBox(
                height: 50,
              ),
              Container(
                width: _pagewidth * 0.4,
                child: Text(
                  'ShieldBot is a comprehensive application designed for testing web vulnerabilities, including brute force attacks, SQL injection, and DoS simulations.',
                  style: AppStyles.bodyStyle,
                ),
              )
            ],
          ),
        ],
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
      height: _pageheight * 0.8,
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
                        fontSize: 68,
                        fontFamily: 'Nohemi',
                        fontWeight: FontWeight.w600,
                        color: Colors.white,
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
                        padding: WidgetStatePropertyAll(EdgeInsets.all(30)),
                        backgroundColor: WidgetStatePropertyAll(
                            const Color.fromARGB(116, 108, 97, 97)),
                        elevation: WidgetStatePropertyAll(10),
                        shape: WidgetStatePropertyAll(
                          RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(10)),
                        ),
                      ),
                      onPressed: () {
                        context.go('/dashboard');
                      },
                      child: Text('Check Now', style: AppStyles.bodyStyle),
                    ),
                    SizedBox(
                      width: 60,
                    ),
                    ElevatedButton(
                      style: ButtonStyle(
                        padding: WidgetStatePropertyAll(EdgeInsets.all(30)),
                        backgroundColor: WidgetStatePropertyAll(
                            const Color.fromARGB(116, 108, 97, 97)),
                        elevation: WidgetStatePropertyAll(10),
                        shape: WidgetStatePropertyAll(
                          RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(10)),
                        ),
                      ),
                      onPressed: () {},
                      child: Text('Browse Features',
                          style: AppStyles.bodyStyle
                              .copyWith(color: Colors.white54)),
                    ),
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
