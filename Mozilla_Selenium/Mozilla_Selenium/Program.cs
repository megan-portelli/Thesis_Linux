using OpenQA.Selenium.Firefox;

/// <summary>
/// This project will be to simulate a Gold Standard Parser, which
/// in this case will be the Mozilla Firefox Parser. It will be tested
/// by simply performing a search on the Mozilla Firefox browser and
/// any exceptions will be recorded in a text file for further investigation.
/// </summary>

List<string> inputs = System.IO.File.ReadAllLines("C:\\Users\\Win10 User\\source\\repos\\Thesis_Linux\\Mozilla_Selenium\\Mozilla_Selenium\\Inputs\\mutational_urls.txt").ToList();
string resultFilePath = "C:\\Users\\Win10 User\\source\\repos\\Thesis_Linux\\Mozilla_Selenium\\Mozilla_Selenium\\Results\\MutationalResults.txt";
string logsFilePath = "C:\\Users\\Win10 User\\source\\repos\\Thesis_Linux\\Mozilla_Selenium\\Mozilla_Selenium\\Logs\\MutationalLogs.txt";

var options = new FirefoxOptions();

//Opening browser
var driver = new FirefoxDriver(options);
driver.Manage().Window.Maximize();

foreach(string input in inputs)
{
    try
    {
        File.AppendAllText(logsFilePath, "Starting process for URL: " + input + "\n");
        driver.Navigate().GoToUrl(input);
        File.AppendAllText(logsFilePath, "URL: " + input + "parsed successfully\n");
    }
    catch (OpenQA.Selenium.WebDriverArgumentException webDriverArgEx)
    {
        File.AppendAllText(resultFilePath, "URL: " + input +" "+ webDriverArgEx.Message + "\n");
    }
    catch (OpenQA.Selenium.WebDriverException webDriverEx)
    {
        File.AppendAllText(resultFilePath, "URL: " + input + " " + webDriverEx.Message + "\n");
    }
    catch(Exception ex)
    {
        File.AppendAllText(resultFilePath, "URL: " + input + " " + ex.Message + "\n");
    }

}

driver.Quit();