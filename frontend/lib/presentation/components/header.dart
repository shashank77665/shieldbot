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
              style: TextStyle(
                fontSize: 28,
                fontWeight: FontWeight.w900,
                color: Colors.black,
              ),
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
                    style: TextStyle(
                      fontSize: 25,
                      fontWeight: FontWeight.w500,
                      color: const Color.fromARGB(255, 56, 43, 43),
                    ),
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
                    style: TextStyle(
                      fontSize: 25,
                      fontWeight: FontWeight.w500,
                      color: const Color.fromARGB(255, 56, 43, 43),
                    ),
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
                    style: TextStyle(
                      fontSize: 25,
                      fontWeight: FontWeight.w500,
                      color: const Color.fromARGB(255, 56, 43, 43),
                    ),
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 10),
                child: ElevatedButton(
                    style: ButtonStyle(
                        padding: WidgetStatePropertyAll(EdgeInsets.all(15))),
                    onPressed: () {
                      showDialog(
                        context: context,
                        builder: (context) {
                          return AlertDialog(
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
                      style: TextStyle(
                        fontSize: 25,
                        fontWeight: FontWeight.w500,
                        color: const Color.fromARGB(255, 56, 43, 43),
                      ),
                    )),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 10),
                child: ElevatedButton(
                    style: ButtonStyle(
                        padding: WidgetStatePropertyAll(EdgeInsets.all(15))),
                    onPressed: () {},
                    child: Text(
                      'Signup',
                      style: TextStyle(
                        fontSize: 25,
                        fontWeight: FontWeight.w500,
                        color: const Color.fromARGB(255, 56, 43, 43),
                      ),
                    )),
              )
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
        width: widget.widget.pagewidth * 0.3,
        padding: EdgeInsets.all(50),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              decoration: BoxDecoration(
                  color: Colors.white70,
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
                          color:
                              widget.isNewUser ? Colors.white70 : Colors.blue,
                          borderRadius: BorderRadius.circular(10)),
                      child: Text(
                        'Login ',
                        textAlign: TextAlign.center,
                        style: AppStyles.headingStyle,
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
                          color:
                              widget.isNewUser ? Colors.blue : Colors.white10,
                          borderRadius: BorderRadius.circular(10)),
                      child: Text(
                        'Signup ',
                        textAlign: TextAlign.center,
                        style: AppStyles.headingStyle,
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
                border: OutlineInputBorder(),
                hintText: 'Username',
                label: Text('Username')),
          ),
        ),
        SizedBox(
          height: 20,
        ),
        SizedBox(
          width: widget.pagewidth * 0.18,
          child: TextField(
            decoration: InputDecoration(
                border: OutlineInputBorder(),
                hintText: 'Password',
                label: Text('Password')),
          ),
        ),
        SizedBox(
          height: 20,
        ),
        ElevatedButton(
            onPressed: () {},
            style: ButtonStyle(
                minimumSize:
                    WidgetStatePropertyAll(Size(widget.pagewidth * 0.18, 60))),
            child: Text('Login')),
        SizedBox(
          height: 20,
        ),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [Text('Forgot Password'), Text('New User')],
        )
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
                border: OutlineInputBorder(),
                hintText: 'Username',
                label: Text('Username')),
          ),
        ),
        SizedBox(
          height: 20,
        ),
        SizedBox(
          width: widget.pagewidth * 0.18,
          child: TextField(
            decoration: InputDecoration(
                border: OutlineInputBorder(),
                hintText: 'Password',
                label: Text('Password')),
          ),
        ),
        SizedBox(
          height: 20,
        ),
        SizedBox(
          width: widget.pagewidth * 0.18,
          child: TextField(
            decoration: InputDecoration(
                border: OutlineInputBorder(),
                hintText: 'Confirm Password',
                label: Text('Confirm Password')),
          ),
        ),
        SizedBox(
          height: 20,
        ),
        ElevatedButton(
            onPressed: () {},
            style: ButtonStyle(
                minimumSize:
                    WidgetStatePropertyAll(Size(widget.pagewidth * 0.18, 60))),
            child: Text('Signup')),
        SizedBox(
          height: 10,
        ),
        Row(
          mainAxisAlignment: MainAxisAlignment.end,
          children: [Text('Existing User')],
        )
      ],
    );
  }
}
