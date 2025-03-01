import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:shieldbot/presentation/components/styles.dart';

class Header extends StatefulWidget {
  final double pageheight;
  final double pagewidth;
  const Header({
    super.key,
    required double this.pageheight,
    required double this.pagewidth,
  });

  @override
  State<Header> createState() => _HeaderState();
}

class _HeaderState extends State<Header> {
  bool isNewUser = false;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 20),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        mainAxisSize: MainAxisSize.max,
        children: [
          GestureDetector(
            onTap: () {
              context.go('/landing');
            },
            child: Text(
              'shieldBot',
              style: AppStyles.subheadingStyle,
            ),
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            crossAxisAlignment: CrossAxisAlignment.center,
            mainAxisSize: MainAxisSize.max,
            children: [
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 10),
                child: GestureDetector(
                  onTap: () {
                    context.go('/ourServices');
                  },
                  child: Text(
                    'Our Services',
                    style: AppStyles.subheadingStyle
                        .copyWith(fontSize: 20, color: Colors.white38),
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 10),
                child: GestureDetector(
                  onTap: () {
                    context.go('/faq');
                  },
                  child: Text(
                    'FAQ',
                    style: AppStyles.subheadingStyle
                        .copyWith(fontSize: 20, color: Colors.white38),
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 10),
                child: GestureDetector(
                  onTap: () {
                    context.go('/aboutUs');
                  },
                  child: Text(
                    'About Us',
                    style: AppStyles.subheadingStyle
                        .copyWith(fontSize: 20, color: Colors.white38),
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 10),
                child: GestureDetector(
                  onTap: () {
                    showDialog(
                      context: context,
                      builder: (context) {
                        return AlertDialog(
                          contentPadding: EdgeInsets.zero,
                          insetPadding: EdgeInsets.zero,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.zero,
                          ),
                          elevation: 10,
                          shadowColor: Colors.black.withOpacity(0.5),
                          content: _authDialog(
                            widget: widget,
                            isNewUser: isNewUser,
                          ),
                        );
                      },
                    );
                  },
                  child: Text(
                    'Login',
                    style: AppStyles.subheadingStyle
                        .copyWith(fontSize: 20, color: Colors.white),
                  ),
                ),
              ),
            ],
          )
        ],
      ),
    );
  }
}

class _authDialog extends StatefulWidget {
  bool isNewUser;
  _authDialog({
    super.key,
    required this.widget,
    required this.isNewUser,
  });

  final Header widget;

  @override
  State<_authDialog> createState() => _authDialogState();
}

class _authDialogState extends State<_authDialog> {
  @override
  Widget build(BuildContext context) {
    return Container(
        // height: widget.widget.pageheight * 0.6,
        width: widget.widget.pagewidth * 0.6,
        child: Row(
          children: [
            Container(
              width: widget.widget.pagewidth * 0.3,
              height: widget.widget.pageheight * 0.6,
              decoration:
                  BoxDecoration(color: Color.fromARGB(255, 234, 229, 254)),
              child: Image.asset(
                  '/Volumes/Data/Projects/shieldbot/frontend/assets/images/useronboarding.png'),
            ),
            Container(
              width: widget.widget.pagewidth * 0.3,
              height: widget.widget.pageheight * 0.6,
              decoration: BoxDecoration(color: AppStyles.secondaryBackground),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.center,
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Container(
                    decoration: BoxDecoration(
                        color: AppStyles.info,
                        border: Border.all(color: Colors.black),
                        borderRadius: BorderRadius.circular(10)),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        GestureDetector(
                          onTap: () {
                            widget.isNewUser = false;
                            setState(() {});
                          },
                          child: Container(
                            padding: EdgeInsets.all(15),
                            width: widget.widget.pagewidth * 0.09,
                            decoration: BoxDecoration(
                                color: widget.isNewUser
                                    ? AppStyles.info
                                    : Colors.white,
                                borderRadius: BorderRadius.circular(10)),
                            child: Text(
                              'Login ',
                              textAlign: TextAlign.center,
                              style: AppStyles.bodyStyle.copyWith(
                                  color: widget.isNewUser
                                      ? Colors.white
                                      : Colors.black),
                            ),
                          ),
                        ),
                        GestureDetector(
                          onTap: () {
                            widget.isNewUser = true;
                            setState(() {});
                          },
                          child: Container(
                            padding: EdgeInsets.all(15),
                            width: widget.widget.pagewidth * 0.09,
                            decoration: BoxDecoration(
                                color: widget.isNewUser
                                    ? Colors.white
                                    : AppStyles.info,
                                borderRadius: BorderRadius.circular(10)),
                            child: Text(
                              'Signup ',
                              textAlign: TextAlign.center,
                              style: AppStyles.bodyStyle.copyWith(
                                  color: widget.isNewUser
                                      ? Colors.black
                                      : Colors.white),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  widget.isNewUser
                      ? _signupWidget(widget: widget.widget)
                      : _loginWidget(widget: widget.widget)
                ],
              ),
            ),
          ],
        ));
  }
}

class _loginWidget extends StatelessWidget {
  const _loginWidget({
    super.key,
    required this.widget,
  });

  final Header widget;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        SizedBox(
          height: 20,
        ),
        SizedBox(
          width: widget.pagewidth * 0.18,
          child: TextField(
            decoration: InputDecoration(
              hintText: 'Username',
              labelText: 'Username',
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
                borderSide: BorderSide(color: Colors.white, width: 2),
              ),
            ),
            style: TextStyle(color: Colors.white),
          ),
        ),
        SizedBox(
          height: 20,
        ),
        SizedBox(
          width: widget.pagewidth * 0.18,
          child: TextField(
            decoration: InputDecoration(
              hintText: 'Password',
              labelText: 'Password',
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
                borderSide: BorderSide(color: Colors.white, width: 2),
              ),
            ),
            style: TextStyle(color: Colors.white),
          ),
        ),
        SizedBox(
          height: 20,
        ),
        ElevatedButton(
          style: ButtonStyle(
            padding: WidgetStatePropertyAll(EdgeInsets.all(20)),
            backgroundColor: WidgetStatePropertyAll(Colors.white),
            elevation: WidgetStatePropertyAll(10),
            shape: WidgetStatePropertyAll(
              RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
            ),
          ),
          onPressed: () {},
          child: Text('Login',
              style: AppStyles.bodyStyle.copyWith(color: Colors.black)),
        ),
        SizedBox(
          height: 15,
        ),
        Row(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            Spacer(),
            Text(
              'Forgot Password',
              style: TextStyle(
                color: const Color.fromARGB(91, 241, 174, 5),
              ),
              textAlign: TextAlign.start,
            ),
            Spacer()
          ],
        ),
      ],
    );
  }
}

class _signupWidget extends StatelessWidget {
  const _signupWidget({
    super.key,
    required this.widget,
  });

  final Header widget;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        SizedBox(
          height: 20,
        ),
        SizedBox(
          width: widget.pagewidth * 0.18,
          child: TextField(
            decoration: InputDecoration(
              hintText: 'Username',
              labelText: 'Username',
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
                borderSide: BorderSide(color: Colors.white, width: 2),
              ),
            ),
            style: TextStyle(color: Colors.white),
          ),
        ),
        SizedBox(
          height: 20,
        ),
        SizedBox(
          width: widget.pagewidth * 0.18,
          child: TextField(
            decoration: InputDecoration(
              hintText: 'Password',
              labelText: 'Password',
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
                borderSide: BorderSide(color: Colors.white, width: 2),
              ),
            ),
            style: TextStyle(color: Colors.white),
          ),
        ),
        SizedBox(
          height: 20,
        ),
        SizedBox(
          width: widget.pagewidth * 0.18,
          child: TextField(
            decoration: InputDecoration(
              hintText: 'Confirm Password',
              labelText: 'Confirm Password',
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
                borderSide: BorderSide(color: Colors.white, width: 2),
              ),
            ),
            style: TextStyle(color: Colors.white),
          ),
        ),
        SizedBox(
          height: 20,
        ),
        ElevatedButton(
          style: ButtonStyle(
            padding: WidgetStatePropertyAll(EdgeInsets.all(20)),
            backgroundColor: WidgetStatePropertyAll(Colors.white),
            elevation: WidgetStatePropertyAll(10),
            shape: WidgetStatePropertyAll(
              RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
            ),
          ),
          onPressed: () {},
          child: Text('Signup',
              style: AppStyles.bodyStyle.copyWith(color: Colors.black)),
        ),
        SizedBox(
          height: 15,
        ),
        // Row(
        //   mainAxisAlignment: MainAxisAlignment.start,
        //   children: [
        //     Spacer(),
        //     Text(
        //       'Forgot Password',
        //       style: TextStyle(
        //         color: const Color.fromARGB(91, 241, 174, 5),
        //       ),
        //       textAlign: TextAlign.start,
        //     ),
        //     Spacer()
        //   ],
        // ),
      ],
    );
  }
}
