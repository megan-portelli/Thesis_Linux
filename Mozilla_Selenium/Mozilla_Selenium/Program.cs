using OpenQA.Selenium.Firefox;

List<string> inputs = System.IO.File.ReadAllLines("C:\\Users\\Win10 User\\source\\repos\\Thesis\\Mozilla_Selenium\\inputs.txt").ToList();

var options = new FirefoxOptions();

//Opening browser
var driver = new FirefoxDriver(options);
driver.Manage().Window.Maximize();

try
{
    foreach (string input in inputs)
    {
        driver.Navigate().GoToUrl(input);
    }

}
catch (Exception ex)
{
    Console.WriteLine(ex.ToString());
}

//Closing Browser
driver.Quit();