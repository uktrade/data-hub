var login = require('../login');


casper.test.begin('Login to Datahub', 1, function suite(test) {
  casper.start();
  login.datahub(casper).then(function () {
    this.waitForSelector('.user-name', function () {
      test.assertEval(function () {
        return document.querySelector('span.user-name').textContent == 'Test User:';
      }, 'Correct user appears to be logged in');
    });
  });
  casper.run(function () {
      test.done();
  });
});

casper.test.begin('Login to CDMS', 1, function suite(test) {
  casper.start();
  login.cdms(casper).then(function () {
    test.assertEval(function () {
      return document.querySelectorAll('ul')[1].id == 'Mscrm.DashboardTab';
    }, 'Dynamics dashboard appears to be present');
  })
  casper.run(function () {
      test.done();
  });
});
