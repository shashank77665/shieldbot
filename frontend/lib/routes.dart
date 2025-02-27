import 'package:go_router/go_router.dart';
import 'package:shieldbot/presentation/aboutUs.dart';
import 'package:shieldbot/presentation/dashboard.dart';
import 'package:shieldbot/presentation/faq.dart';
import 'package:shieldbot/presentation/landigPage.dart';
import 'package:shieldbot/presentation/ourServices.dart';

final GoRouter appRouter = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => Dashboard(),
    ),
    GoRoute(
      path: '/landing',
      builder: (context, state) => LandingPage(),
    ),
    GoRoute(
      path: '/aboutUs',
      builder: (context, state) => AboutUsPage(),
    ),
    GoRoute(
      path: '/faq',
      builder: (context, state) => faqPage(),
    ),
    GoRoute(
      path: '/ourServices',
      builder: (context, state) => ourServicesPage(),
    ),
    GoRoute(
      path: '/dashboard',
      builder: (context, state) => Dashboard(),
    ),
  ],
);
