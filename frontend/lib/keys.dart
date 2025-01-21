import 'package:flutter_dotenv/flutter_dotenv.dart';

final backend_url = dotenv.env['BACKEND_URL'] ?? 'http://127.0.0.1:5000';
