import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:shieldbot/presentation/aboutUs.dart';

class Header extends StatelessWidget {
  const Header({
    super.key,
  });

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
                    onPressed: () {},
                    child: Text(
                      'Login',
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
