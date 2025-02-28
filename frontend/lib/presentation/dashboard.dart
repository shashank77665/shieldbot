import 'package:flutter/material.dart';
import 'package:shieldbot/presentation/components/footer.dart';
import 'package:shieldbot/presentation/components/header.dart';
import 'package:shieldbot/presentation/components/styles.dart';

class Dashboard extends StatefulWidget {
  const Dashboard({super.key});

  @override
  State<Dashboard> createState() => _DashboardState();
}

class _DashboardState extends State<Dashboard> {
  @override
  Widget build(BuildContext context) {
    final _pageheight = MediaQuery.of(context).size.height;
    final _pagewidth = MediaQuery.of(context).size.width;

    return Scaffold(
      body: Container(
        padding: EdgeInsets.symmetric(horizontal: _pagewidth * 0.1),
        decoration: AppStyles.containerDecoration,
        child: SingleChildScrollView(
          child: Column(
            children: [
              Header(pageheight: _pageheight, pagewidth: _pagewidth),
              Container(
                height: _pageheight,
                child: Container(
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.all(Radius.circular(10)),
                  ),
                  padding: EdgeInsets.all(50),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      Row(
                        mainAxisSize: MainAxisSize.max,
                        mainAxisAlignment: MainAxisAlignment.end,
                        children: [
                          ElevatedButton(
                              onPressed: () {}, child: Text('New Attack'))
                        ],
                      ),
                      Container(
                        height: _pageheight * 0.8,
                        decoration: BoxDecoration(
                          color: Colors.cyan,
                          borderRadius: BorderRadius.all(Radius.circular(10)),
                        ),
                        padding: EdgeInsets.all(50),
                        child: Container(
                          decoration: BoxDecoration(
                            color: const Color.fromARGB(255, 238, 216, 216),
                            borderRadius: BorderRadius.all(Radius.circular(10)),
                          ),
                          child: Row(
                            mainAxisSize: MainAxisSize.max,
                            crossAxisAlignment: CrossAxisAlignment.start,
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              _recentTasks(pagewidth: _pagewidth),
                              _taskStatus(pagewidth: _pagewidth),
                            ],
                          ),
                        ),
                      )
                    ],
                  ),
                ),
              ),
              Footer()
            ],
          ),
        ),
      ),
    );
  }
}

class _taskStatus extends StatelessWidget {
  const _taskStatus({
    super.key,
    required double pagewidth,
  }) : _pagewidth = pagewidth;

  final double _pagewidth;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(10),
      width: _pagewidth * 0.45,
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.all(Radius.circular(10)),
      ),
      child: Column(
        children: [
          Text(
            'Attack Status',
            style: AppStyles.headingStyle,
          ),
        ],
      ),
    );
  }
}

class _recentTasks extends StatelessWidget {
  const _recentTasks({
    super.key,
    required double pagewidth,
  }) : _pagewidth = pagewidth;

  final double _pagewidth;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(10),
      width: _pagewidth * 0.2,
      decoration: BoxDecoration(
        color: const Color.fromARGB(255, 238, 216, 216),
        borderRadius: BorderRadius.all(Radius.circular(10)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                'Recent Tasks',
                style: AppStyles.headingStyle,
              ),
            ],
          ),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'taskid - 1232 bruteforce',
                textAlign: TextAlign.start,
              ),
              Text('taskid - 1232 bruteforce'),
              Text('taskid - 1232 bruteforce'),
              Text('taskid - 1232 bruteforce'),
              Text('taskid - 1232 bruteforce'),
              Text('taskid - 1232 bruteforce'),
              Text('taskid - 1232 bruteforce')
            ],
          )
        ],
      ),
    );
  }
}
