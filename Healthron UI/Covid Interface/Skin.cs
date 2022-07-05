using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Covid_Interface
{
    public partial class Skin : Form
    {
        public Skin()
        {
            InitializeComponent();
        }

        private void Skin_Load(object sender, EventArgs e)
        {
           
        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {
            System.Diagnostics.Process.Start(@"C:\Program Files\Innovation projects\CovidEnforcement\MaskCheck\MaskCheck\S_monkeyPox.bat");

        }

        private void label6_Click(object sender, EventArgs e)
        {
            System.Diagnostics.Process.Start(@"C:\Program Files\Innovation projects\CovidEnforcement\MaskCheck\MaskCheck\S_monkeyPox.bat");
        }

        private void label5_Click(object sender, EventArgs e)
        {
            Main main = new Main(); 
            main.Show();
            this.Close();
        }
    }
}
