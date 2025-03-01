import 'package:flutter/material.dart';
import 'package:shieldbot/presentation/components/styles.dart';

class Footer extends StatelessWidget {
  const Footer({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 100),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'We Are Located At ',
                style: AppStyles.subheadingStyle,
              ),
              Text(
                'Near Kharar Bus Stand, Kharar',
                style: AppStyles.bodyStyle,
              ),
              Text(
                'SAS Nagar, Punjab (140301)',
                style: AppStyles.bodyStyle,
              )
            ],
          ),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Contact Us ',
                style: AppStyles.subheadingStyle,
              ),
              Text(
                'shashank77665@gmail.com',
                style: AppStyles.bodyStyle,
              )
            ],
          )
        ],
      ),
    );
  }
}
