
//package Main;

import java.awt.Color;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import static javax.swing.WindowConstants.DISPOSE_ON_CLOSE;

public class Main extends JFrame implements ActionListener 
{

    private JLabel countryL;
    private JTextArea countryF;
    private JLabel subjectL;
    private JTextArea subjectF;
    private JButton confirm;
    private JCheckBox custom;
    private JCheckBox extra;
    private JCheckBox uni_grade;
    private JCheckBox major;
    private JCheckBox tips;
    private JLabel outputL;

    private JPanel panel = new JPanel(new GridBagLayout());
    private GridBagConstraints gbc = new GridBagConstraints();

    public Main() 
    {
        
        super("GUI");
        this.setBounds(600, 200, 600, 600); // Adjusted the size to fit the components
        this.getContentPane().setBackground(Color.GRAY);
        panel.setBackground(Color.GRAY);
        this.setDefaultCloseOperation(DISPOSE_ON_CLOSE);

        // Set up GridBagConstraints
        gbc.insets = new Insets(10, 10, 10, 10); // Padding around components
        gbc.anchor = GridBagConstraints.CENTER;
        gbc.fill = GridBagConstraints.HORIZONTAL;
        gbc.weightx = 1.0;
        gbc.weighty = 0.0;

        // Initialize components
        this.countryL = new JLabel("What country(ies) do you want to major? Separate countries with a comma (,)");
        this.subjectL = new JLabel("What major(s) do you want to major? Separate majors with a comma (,)");
        this.outputL = new JLabel();

        this.confirm = new JButton("Confirm");
        this.custom = new JCheckBox("Custom Question");
        this.extra = new JCheckBox("Extra Curricular recommendations");
        this.uni_grade = new JCheckBox("Good universities based on your grades");
        this.major = new JCheckBox("Major recommendations");
        this.tips = new JCheckBox("Tips of what you should do");

        this.countryF = new JTextArea(5, 40); // 5 rows, 40 columns
        this.subjectF = new JTextArea(5, 40); // 5 rows, 40 columns
        JScrollPane countryScrollPane = new JScrollPane(countryF);
        JScrollPane subjectScrollPane = new JScrollPane(subjectF);

        confirm.addActionListener(this);
        
        custom.setOpaque(false);
        extra.setOpaque(false);
        uni_grade.setOpaque(false);
        major.setOpaque(false);
        tips.setOpaque(false);

        // Add components to the panel
        gbc.gridx = 0;
        gbc.gridy = 0;
        panel.add(countryL, gbc);

        gbc.gridy = 1;
        panel.add(countryScrollPane, gbc);

        gbc.gridy = 2;
        panel.add(subjectL, gbc);

        gbc.gridy = 3;
        panel.add(subjectScrollPane, gbc);

        gbc.gridy = 4;
        panel.add(custom, gbc);

        gbc.gridy = 5;
        panel.add(extra, gbc);

        gbc.gridy = 6;
        panel.add(uni_grade, gbc);

        gbc.gridy = 7;
        panel.add(major, gbc);

        gbc.gridy = 8;
        panel.add(tips, gbc);

        gbc.gridy = 9;
        panel.add(confirm, gbc);

        gbc.gridy = 10;
        gbc.weighty = 1.0;
        gbc.fill = GridBagConstraints.BOTH;
        panel.add(outputL, gbc);

        this.add(panel);
        this.setVisible(true);
    }

    public static void main(String[] args) {
        new Main();
    }

    @Override
    public void actionPerformed(ActionEvent e) 
    {
        
        String command = e.getActionCommand();
        if (command.equals("Confirm")) 
        {
            String pythonMethod = "";
            String prompt = "";
            if (custom.isSelected()) 
            {
                prompt = "custom";
            } else if (extra.isSelected()) 
            {
                prompt = "extra";
            } else if (uni_grade.isSelected()) 
            {
                prompt = "possible";
            } else if (major.isSelected()) 
            {
                prompt = "major";
            } else if (tips.isSelected()) 
            {
                prompt = "tips";
            }

            String country = countryF.getText().trim();
            String subject = subjectF.getText().trim();
            String[] pythonCommand = {"python", "script.py", prompt, country, subject};

            try 
            {
                // Start the process
                ProcessBuilder pb = new ProcessBuilder(pythonCommand);
                pb.redirectErrorStream(true); // Redirect error stream to the output stream
                Process p = pb.start();

                // Read the output from the process
                BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream(), "UTF-8"));
                StringBuilder output = new StringBuilder();
                String result;
                while ((result = in.readLine()) != null) 
                {
                    output.append(result).append("\n");
                }
                in.close();

                // Process the output to extract text
                String outputText = extractTextFromOutput(output.toString());
                
                // Update JLabel with the output from the Python script
                outputL.setText("<html>" + outputText + "</html>");

                // Check for process exit status
                int exitCode = p.waitFor();
                System.out.println("Python script exited with code: " + exitCode);

            } 
            
            catch (IOException se) 
            {
                System.err.println("IOException occurred: " + se.getMessage());
                se.printStackTrace();
            } 
            
            catch (InterruptedException se) 
            {
                System.err.println("InterruptedException occurred: " + se.getMessage());
                se.printStackTrace();
            } 
            
            catch (Exception se) 
            {
                se.printStackTrace();
            }
            
        }
        
    }

    private String extractTextFromOutput(String output) {
        // Extract text from the output format
        String[] lines = output.split("\n");
        StringBuilder formattedText = new StringBuilder();
        for (String line : lines) {
            if (line.contains("TextBlock(text=")) {
                int start = line.indexOf("text='") + 6;
                int end = line.indexOf("'", start);
                if (start > 0 && end > start) {
                    formattedText.append(line.substring(start, end)).append(" ");
                }
            }
        }
        // Remove any excessive newlines and trim leading/trailing spaces
        return formattedText.toString().replaceAll("\\s+", " ").trim();
    }
}