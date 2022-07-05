namespace Covid_Interface
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

       

        private void button3_Click(object sender, EventArgs e)
        {
            Main main1 = new Main();
            main1.Show();
            //this.Close();
        }
    }
}