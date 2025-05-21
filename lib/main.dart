// main.dart
import 'package:flutter/material.dart';
import 'screens/home_screen.dart';
import 'screens/assistant_screen.dart';
import 'screens/events_screen.dart';
import 'package:google_nav_bar/google_nav_bar.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Muslim Assistant',
      theme: ThemeData.dark(),
      home: MainPage(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class MainPage extends StatefulWidget {
  @override
  _MainPageState createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  int _currentIndex = 0;
  final List<Widget> _screens = [
    HomeScreen(),
    AssistantScreen(),
    EventsScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_currentIndex],
      bottomNavigationBar: Container(
  decoration: BoxDecoration(
    color: Colors.black,
    boxShadow: [BoxShadow(blurRadius: 20, color: Colors.black.withOpacity(0.3))],
  ),
  child: Padding(
    padding: const EdgeInsets.symmetric(horizontal: 15.0, vertical: 12),
    child: GNav(
      backgroundColor: Colors.black,
      color: Colors.grey[400],
      activeColor: Colors.white,
      tabBackgroundColor: Colors.grey[800]!,
      gap: 8,
      padding: EdgeInsets.symmetric(horizontal: 20, vertical: 12),
      selectedIndex: _currentIndex,
      onTabChange: (index) {
        setState(() => _currentIndex = index);
      },
      tabs: const [
        GButton(icon: Icons.menu_book, text: 'Hadith'),
        GButton(icon: Icons.chat_bubble_outline, text: 'Ask'),
        GButton(icon: Icons.location_on_outlined, text: 'Events'),
      ],
    ),
  ),
),
    );
  }
  
}
