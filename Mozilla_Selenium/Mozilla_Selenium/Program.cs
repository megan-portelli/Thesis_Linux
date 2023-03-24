using OpenQA.Selenium.Firefox;

/// <summary>
/// This project will be to simulate a Golden Standard Parser, which
/// in this case will be the Mozilla Firefox Parser. It will be tested
/// by simply performing a search on the Mozilla Firefox browser and
/// any exceptions will be recorded in a text file for further investigation.
/// </summary>

List<string> inputs = System.IO.File.ReadAllLines("C:\\Users\\Win10 User\\source\\repos\\Thesis_Linux\\Mozilla_Selenium\\Mozilla_Selenium\\Inputs\\inputs.txt").ToList();
string resultFilePath = "C:\\Users\\Win10 User\\source\\repos\\Thesis_Linux\\Mozilla_Selenium\\Mozilla_Selenium\\Results\\results.txt";

var options = new FirefoxOptions();

//Opening browser
var driver = new FirefoxDriver(options);
driver.Manage().Window.Maximize();

foreach(string input in inputs)
{
    try
    {
        driver.Navigate().GoToUrl(input);
    }
    catch (OpenQA.Selenium.WebDriverArgumentException webDriverArgEx)
    {
        File.AppendAllText(resultFilePath, "\nURL: " + input +" "+ webDriverArgEx.Message);
    }
    catch (OpenQA.Selenium.WebDriverException webDriverEx)
    {
        File.AppendAllText(resultFilePath, "\nURL: " + input + " " + webDriverEx.Message);
    }
    catch(Exception ex)
    {
        File.AppendAllText(resultFilePath, "\nURL: " + input + " " + ex.Message);
    }

}

//Closing Browser
driver.Quit();