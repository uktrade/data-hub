var env = require('system').env;

var cdms = function (casper) {
  casper.open(env.CDMS_BASE_URL).then(function () {
    this.waitForSelector(
      '#bcSignout',
      function noop () {
        this.echo('Already logged in', 'TRACE');
      },
      function submitCredentials () {
        this.waitForSelector(
          '#ctl00_ContentPlaceHolder1_PassiveIdentityProvidersDropDownList',
          function () {
            this.fill(
              'form#aspnetForm',
              {
                ctl00$ContentPlaceHolder1$PassiveIdentityProvidersDropDownList: env.CDMS_ADFS_URL,
              },
              true
            );
          }
        );
        casper.then(function () {
          this.click('#ctl00_ContentPlaceHolder1_PassiveSignInButton');
        });
        casper.waitForSelector('#ContentPlaceHolder1_SubmitButton',
          function () {
            this.sendKeys('#ContentPlaceHolder1_UsernameTextBox', env.CDMS_USERNAME);
            this.sendKeys('#ContentPlaceHolder1_PasswordTextBox', env.CDMS_PASSWORD);
            this.click('#ContentPlaceHolder1_SubmitButton');
          }
        );
        casper.waitForSelector(
          '#bcSignout',
          function () {
            this.echo('Logged in OK', 'TRACE');
            this.thenOpen(env.CDMS_BASE_URL + '/main.aspx')
          },
          function () {
            this.echo('CDMS login failed, trying again', 'ERROR');
            cdms(this);
          },
          5000
        );
      });
    });
  return casper;
};

var datahub = function (casper) {
  casper.open('http://10.1.66.99:3000/login').then(function () {
    this.waitForSelector(
      'div.login-bar',
      function noop () {
        this.echo('Already logged in', 'TRACE');
      },
      function submitCredentials () {
        this.waitForSelector('button[type=submit]',
          function () {
            this.sendKeys('#username', env.CDMS_USERNAME);
            this.sendKeys('#password', env.CDMS_PASSWORD);
            this.click('button[type=submit]');
          }
        );
        this.waitForSelector(
          'div.login-bar',
          function () {
            this.echo('Logged in OK', 'TRACE');
          },
          function () {
            this.echo('Datahub login failed, trying again', 'ERROR');
            datahub(this);
          },
          5000
        );
      }
    );
  });
  return casper;
};

module.exports = {cdms: cdms, datahub: datahub};
