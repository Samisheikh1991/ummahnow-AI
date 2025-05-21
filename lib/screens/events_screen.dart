// screens/events_screen.dart
import 'package:flutter/material.dart';

class EventsScreen extends StatelessWidget {
  final String currentZip = "30301"; // You can later make this dynamic

  final List<Map<String, String>> dummyEvents = [
    {
      "title": "Youth Halaqa with Imam Ahmed",
      "location": "Masjid Al-Falah",
      "distance": "7 mi",
      "time": "Friday, 7 PM"
    },
    {
      "title": "Islamic Conference: Faith in Action",
      "location": "ICNF Center",
      "distance": "12 mi",
      "time": "Saturday, 2 PM"
    },
    {
      "title": "Eid Bazaar & Food Drive",
      "location": "Masjid Umar Bin Khattab",
      "distance": "18 mi",
      "time": "Sunday, 11 AM"
    }
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Events Near $currentZip')),
      body: ListView.builder(
        itemCount: dummyEvents.length,
        itemBuilder: (context, index) {
          final event = dummyEvents[index];
          return Card(
            margin: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: ListTile(
              title: Text(event['title'] ?? ''),
              subtitle: Text("${event['location']} • ${event['time']}"),
              trailing: Text(event['distance'] ?? ''),
            ),
          );
        },
      ),
    );
  }
}