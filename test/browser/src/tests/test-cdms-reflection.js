var login = require('../login');


casper.test.begin('Company', 1, function suite(test) {
  casper.start();
  login.datahub(casper).then(function () {
    // search for company
    // click on it
    // assert it has the expected name etc
    // edit something
    // assert edits held
    // assert edits held on cdms
    test.assert(false);
  });
  casper.run(function () {
      test.done();
  });
});

casper.test.begin('Contact', 1, function suite(test) {
  casper.start();
  login.datahub(casper).then(function () {
    // search for contact
    // click on it
    // assert it has the expected name etc
    // edit something
    // assert edits held
    // assert edits held on cdms
    test.assert(false);
  });
  casper.run(function () {
      test.done();
  });
});

casper.test.begin('Interaction', 1, function suite(test) {
  casper.start();
  login.datahub(casper).then(function () {
    // search for company
    // click on it
    // click on interactions
    // assert it has the expected name etc
    // edit something
    // assert edits held
    // assert edits held on cdms
    test.assert(false);
  });
  casper.run(function () {
      test.done();
  });
});

