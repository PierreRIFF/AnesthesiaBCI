import java.io.*;
import java.net.*;
import java.nio.*;

/*
 * Primitive TCP Tagging java client for OpenViBE 1.2.x
 *
 * @author Jussi T. Lindgren / Inria
 * @date 04.Jul.2016
 * @version 0.1
 * @todo Add error handling
 */
class StimulusSender
{
  Socket m_clientSocket;
  DataOutputStream m_outputStream;
 
  // Open connection to Acquisition Server TCP Tagging 
  boolean open(String host, Integer port) throws Exception
  {
    m_clientSocket = new Socket(host, port);
    m_outputStream = new DataOutputStream(m_clientSocket.getOutputStream());

    return true;
  }

  // Close connection
  boolean close() throws Exception 
  {
    m_clientSocket.close();

    return true;
  }

  // Send stimulation with a timestamp. 
  boolean send(Long stimulation, Long timestamp) throws Exception
  {
    ByteBuffer b = ByteBuffer.allocate(24);
    b.order(ByteOrder.LITTLE_ENDIAN); // Assumes AS runs on LE architecture
    b.putLong(0);              // Not used
    b.putLong(stimulation);    // Stimulation id
    b.putLong(timestamp);      // Timestamp: 0 = immediate
  
    m_outputStream.write(b.array());

    return true;
  }

  public static void main(String argv[]) throws Exception
  {
    StimulusSender sender = new StimulusSender();

    sender.open("localhost", 15361);
 
    // Send identity of the event (stimulation id), time of occurrence. 
    // The preferred mechanism is to use time '0' and call the send() 
    // function immediately after each event has been rendered/played.
    sender.send(123L, 0L);  // Some event
    sender.send(666L, 0L);  // Another one...

    // etc ...

    // To verify that the stimulations are received correctly by
    // AS, set LogLevel to Trace in 'openvibe.conf' before running AS.
    // Note that instead of stamp=0, AS may print the stamp it replaces 
    // the 0 with. Finally, network-acquisition.xml (in box-tutorials/) 
    // scenario can be used to display the events in Designer as combined
    // with the signal, for example using the Generic Oscillator driver
    // in AS.

    sender.close();
  }
}

