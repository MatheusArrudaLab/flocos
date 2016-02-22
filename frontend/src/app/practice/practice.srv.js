/**
 * Practice Session Service
 * @ngInject
 */
angular.module('flocs.practice')
.factory('practiceService', function ($state, $timeout, $q, practiceDao, taskEnvironmentService, userService) {

  var attemptReport = null;
  var taskStartTimestamp = null;
  var taskFinishedDeferred = null;
  var taskInstance = null;
  var session = {
    task: null,
    max: null,
    progress: null,
    active: false
  };

  var attemptEvaluation = {
    earnedCredits: null
  };

  var practiceInfo = {
    available: false,
    totalCredits: null,
    freeCredits: null,
  };

  userService.onUserChange(userChangeListener);

  // === public API ===
  return {
    settingTaskById: settingTaskById,
    settingNextTask: settingNextTask,
    gettingPracticeInfo: gettingPracticeInfo,
    practicingTask: practicingTask,
    taskCompleted: taskCompleted,
    giveUpTask: giveUpTask,
    attemptEvaluation: attemptEvaluation,
    session: session,
    practiceInfo: practiceInfo,
  };

  function userChangeListener() {
    if (userService.isUserAvailable()) {
      gettingPracticeInfo();
    } else {
      practiceInfo.available = false;
    }
  }

  function gettingPracticeInfo() {
    return practiceDao.gettingPracticeDetails().then(function(details) {
      practiceInfo.available = true;
      practiceInfo.totalCredits = details.totalCredits;
      practiceInfo.freeCredits = details.freeCredits;
      practiceInfo.solvedTasksCount = details.solvedTasksCount;
      return practiceInfo;
    }, function() {
      practiceInfo.available = false;
    });
  }

  function settingNextTask() {
    return practiceDao.gettingNextTask().then(function(newTaskInstance) {
      taskInstance = newTaskInstance;
      var newTaskId = taskInstance.task['task-id'];
      var returnedSession = taskInstance['session'];
      session.task = returnedSession.task;
      session.max = returnedSession.max;
      session.progress = (100 / session.max) * (session.task - 1) + 1;
      session.active = true;
      $state.go('practice-task', {'taskId': newTaskId});
    });
  }

  function settingTaskById(taskId) {
    if (taskInstance === null || taskInstance.task['task-id'] != taskId) {
      return practiceDao.gettingTaskById(taskId).then(function (newTaskInstance) {
        taskInstance = newTaskInstance;
        session.active = false;
        startCurrentTask();
        return taskInstance;
      }, function() {
        $state.go('404', null, {'location': false});
      });
    } else {
      return $timeout(function() {
        startCurrentTask();
        return taskInstance;
      });
    }
  }

  function startCurrentTask() {
    userService.setUserAvailable();
    attemptReport = null;
    var newTask = taskInstance['task'];
    newAttemptReport(newTask);
    taskStartTimestamp = Date.now();
    var instructionsText = taskInstance['instructions'];
    taskEnvironmentService.setTask(newTask, attemptFinished,
          instructionsText);
  }

  function giveUpTask() {
    var giveUpReport = {
      'task-instance-id': attemptReport['task-instance-id'],
      'time': calculateSolvingTime()
    };
    attemptReport = null;
    // rejecting the task is postponed after successfuly giving up, in order to
    // make sure the skill has been updated before requesting next task
    practiceDao.sendingGiveUpReport(giveUpReport).then(taskFinishedDeferred.reject);
  }

  /*
   * Start practicing task.
   * The promise is finished only after resolving task.
   */
  function practicingTask() {
    taskFinishedDeferred = $q.defer();
    return taskFinishedDeferred.promise;
  }

  /*
   * Send final report about task resolving including flow report.
   */
  function taskCompleted(taskReport) {
    var flowReport = {
      'task-instance-id': attemptReport['task-instance-id'],
      'flow-report': taskReport['flow']
    };
    practiceDao.sendingFlowReport(flowReport).then(function(result) {
      // reset attempt object
      attemptReport = null;
      // resolve taskFinnished promise
      taskFinishedDeferred.resolve(result);
    });
  }

  function attemptFinished(result) {
    if (attemptReport === null) {
      return;
    }
    if (attemptReport.solved) {
      taskFinishedDeferred.notify(result);
    } else {
      attemptReport.time = calculateSolvingTime();
      attemptReport.attempt += 1;
      attemptReport.solved = result.solved;
      practiceDao.sendingAttemptReport(attemptReport).then(function(response) {
        attemptEvaluation.earnedCredits = response['earned-credits'];
        gettingPracticeInfo();
        taskFinishedDeferred.notify(result);
      });
    }
  }

  /*
   * Return time the user spent solving the task as a number of seconds.
   */
  function calculateSolvingTime() {
    var taskFinishedTimestamp = Date.now();
    var milisecondsSpent = taskFinishedTimestamp - taskStartTimestamp;
    var secondsSpent = Math.ceil(milisecondsSpent / 1000);
    return secondsSpent;
  }


  /*
   * Create new report for new attempt
   */
  function newAttemptReport(task) {
    attemptReport = {
      'task-instance-id': taskInstance['task-instance-id'],
      'attempt': 0,
      'time': 0,
      'solved': false,
    };
  }
});
