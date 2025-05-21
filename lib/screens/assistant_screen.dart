// assistant_screen.dart — Bubble animation + Glow trail + Flask AI backend
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:http/http.dart' as http;

class AssistantScreen extends StatefulWidget {
  @override
  _AssistantScreenState createState() => _AssistantScreenState();
}

class _AssistantScreenState extends State<AssistantScreen> with TickerProviderStateMixin {
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  List<Map<String, dynamic>> chat = [];

  Future<void> getResponse(String input) async {
    setState(() {
      chat.add({"from": "user", "text": input, "glow": true});
    });

    try {
      final res = await http.post(
  Uri.parse('https://8530-2060-1722-5300-fd46-d4d1-df1c-dcc8-67f5.ngrok-free.app/recommend'),
  headers: {"Content-Type": "application/json"},
  body: jsonEncode({"query": input}),
);

      if (res.statusCode == 200) {
        final data = jsonDecode(res.body);
        setState(() {
          chat.add({"from": "bot", "text": data['response']});
        });
      } else {
        setState(() {
          chat.add({"from": "bot", "text": "Something went wrong with the server."});
        });
      }
    } catch (e) {
      setState(() {
        chat.add({"from": "bot", "text": "Failed to connect to AI server."});
      });
    }

    _scrollToBottom();
  }

  void _scrollToBottom() {
    Future.delayed(Duration(milliseconds: 400), () {
      _scrollController.animateTo(
        _scrollController.position.maxScrollExtent,
        duration: Duration(milliseconds: 300),
        curve: Curves.easeOut,
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color(0xFF0F0F0F),
      appBar: AppBar(
        title: Text('Ask UmmahNow', style: GoogleFonts.poppins(fontWeight: FontWeight.bold)),
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              itemCount: chat.length,
              itemBuilder: (context, index) {
                final msg = chat[index];
                final isUser = msg['from'] == 'user';
                return TweenAnimationBuilder(
                  duration: Duration(milliseconds: 400),
                  tween: Tween<Offset>(begin: Offset(0, 0.3), end: Offset.zero),
                  builder: (context, offset, child) {
                    return Transform.translate(
                      offset: offset,
                      child: AnimatedOpacity(
                        opacity: 1,
                        duration: Duration(milliseconds: 400),
                        child: Stack(
                          children: [
                            Align(
                              alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
                              child: Container(
                                margin: EdgeInsets.symmetric(vertical: 6),
                                padding: EdgeInsets.all(12),
                                constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.75),
                                decoration: BoxDecoration(
                                  color: isUser ? Colors.blueAccent : Colors.grey[800],
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                child: Text(
                                  msg['text'],
                                  style: GoogleFonts.poppins(color: Colors.white),
                                ),
                              ),
                            ),
                            if (isUser && msg['glow'] == true)
                              Positioned.fill(child: GlowTrail()),
                          ],
                        ),
                      ),
                    );
                  },
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(12.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    style: TextStyle(color: Colors.white),
                    decoration: InputDecoration(
                      hintText: 'Ask about lectures, prayer, etc...',
                      hintStyle: TextStyle(color: Colors.white60),
                      filled: true,
                      fillColor: Colors.grey[900],
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                        borderSide: BorderSide.none,
                      ),
                    ),
                    onSubmitted: (value) {
                      if (value.trim().isNotEmpty) {
                        getResponse(value.trim());
                        _controller.clear();
                      }
                    },
                  ),
                ),
                SizedBox(width: 8),
                IconButton(
                  icon: Icon(Icons.send, color: Colors.white),
                  onPressed: () {
                    if (_controller.text.trim().isNotEmpty) {
                      getResponse(_controller.text.trim());
                      _controller.clear();
                    }
                  },
                )
              ],
            ),
          )
        ],
      ),
    );
  }
}

class GlowTrail extends StatefulWidget {
  @override
  _GlowTrailState createState() => _GlowTrailState();
}

class _GlowTrailState extends State<GlowTrail> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: Duration(milliseconds: 1000),
    );
    _animation = Tween<double>(begin: 0.0, end: 1.0).animate(_controller);
    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return CustomPaint(
          painter: GlowPainter(progress: _animation.value),
        );
      },
    );
  }
}

class GlowPainter extends CustomPainter {
  final double progress;
  GlowPainter({required this.progress});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.cyanAccent
      ..strokeWidth = 2
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round;

    final length = size.width + size.height * 2;
    final dashLength = 6;
    final gap = 4;
    double current = progress * length;

    final path = Path()
      ..addRRect(RRect.fromRectAndRadius(
        Rect.fromLTWH(0, 0, size.width, size.height), Radius.circular(12)));

    for (final metric in path.computeMetrics()) {
      canvas.drawPath(
        metric.extractPath(current, current + dashLength),
        paint,
      );
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
