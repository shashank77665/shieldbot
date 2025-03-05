import 'dart:convert';
import 'package:http/http.dart' as http;

Future<Map<String, dynamic>?> resolveIP(String domain) async {
  final url = Uri.parse('https://dns.google/resolve?name=$domain');

  try {
    final response = await http.get(url);
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      print('Faid to load data :${response.body}');
    }
  } catch (e) {
    print('Error : $e');
  }
  return null;
}
