import 'package:flutter/material.dart';
import 'package:shieldbot/presentation/components/styles.dart';

class Footer extends StatelessWidget {
  const Footer({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceAround,
      children: [
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'We Are Located At ',
              style: AppStyles.headingStyle,
            ),
            Text(
              'Near Kharar Bus Stand, Kharar',
              style: AppStyles.headingStyle,
            ),
            Text(
              'SAS Nagar, Punjab (140301)',
              style: AppStyles.headingStyle,
            )
          ],
        ),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Contact Us ',
              style: AppStyles.headingStyle,
            ),
            Text(
              'shashank77665@gmail.com',
              style: AppStyles.headingStyle,
            )
          ],
        )
      ],
    );
  }
}
