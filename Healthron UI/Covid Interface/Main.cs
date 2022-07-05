using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Covid_Interface
{
    public partial class Main : Form
    {
        public Main()
        {
            InitializeComponent();
        }

        private void Activate_Click(object sender, EventArgs e)
        {
           

        }
    
       

        private void Activate1_Click(object sender, EventArgs e)
        {
            //non is checked
            if (Mask.Checked == false && Distance1.Checked == false && Temp1.Checked == false && cough1.Checked == false)
            {
                //MessageBox.Show("Make a selection","hjj");
                

            }

            //door
            if (Door1.Checked && Mask.Checked == false && Distance1.Checked == false && Temp1.Checked == false && cough1.Checked == false)
            {
                Process.Start(@"PATH\ TO \S_mask_door.bat");


            }


            //only mask is checked
            if (Mask.Checked && Distance1.Checked == false && Temp1.Checked == false && cough1.Checked == false)
            {
                Process.Start(@"PATH\ TO \S_mask.bat");
                
            }



            //only distance is checked
            if (Mask.Checked == false && Distance1.Checked && Temp1.Checked == false && cough1.Checked == false)
            {
                System.Diagnostics.Process.Start(@"PATH\ TO \S_distance.bat");
            }


            //only thermo
            if (Mask.Checked == false && Distance1.Checked == false && Temp1.Checked && cough1.Checked == false)
            {
                System.Diagnostics.Process.Start(@"PATH\ TO \S_thermo.bat");
            }

            //only cough
            if (Mask.Checked == false && Distance1.Checked == false && Temp1.Checked == false && cough1.Checked)
            {
                System.Diagnostics.Process.Start(@"PATH\ TO \S_cough.bat");
            }

            //only Distance and Mask
            if (Mask.Checked && Distance1.Checked && Temp1.Checked == false && cough1.Checked == false)
            {
                System.Diagnostics.Process.Start(@"PATH\ TO \S_distance_mask.bat");
            }

            //only composure
            if (Mask.Checked == false && Distance1.Checked == false && Temp1.Checked == false && cough1.Checked == false && composure.Checked)
            {
                System.Diagnostics.Process.Start(@"PATH\ TO \S_composure.bat");
            }

            //All
            if (Mask.Checked && Distance1.Checked && Temp1.Checked && cough1.Checked)
            {
                System.Diagnostics.Process.Start(@"PATH\ TO \S_all.bat");
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void label6_Click(object sender, EventArgs e)
        {
            Skin skin = new Skin();
            skin.Show();
            this.Close();
        }


        private void pictureBox1_Click(object sender, EventArgs e)
        {
            Skin skin = new Skin();
            skin.Show();
            this.Close();
        }

        private void pictureBox2_Click(object sender, EventArgs e)
        {
            Skin skin = new Skin();
            skin.Show();
            this.Close();
        }
    }
}
