namespace Setup
{
    public class GpioPinConfig
    {
        public int PinNumber { get; set; }
        public string PinName { get; set; }
        public string FunctionType { get; set; } = "None";
        public string FunctionName { get; set; }
        public int CtrlRegNum { get; set; }
        public int CtrlRegIndex { get; set; }

        public static readonly string[] FunctionTypes = 
        {
            "None", "UART_TX", "UART_RX", "SPI_CLK", "SPI_MOSI", "SPI_MISO", "SPI_CS",
            "I2C_SCL", "I2C_SDA", "PWM", "ADC", "TIMER", "LED", "SWITCH", "GPIO"
        };
    }
}