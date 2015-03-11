package storm.starter;

import backtype.storm.Config;
import backtype.storm.LocalCluster;
import backtype.storm.StormSubmitter;
import backtype.storm.task.ShellBolt;
import backtype.storm.topology.BasicOutputCollector;
import backtype.storm.topology.IRichBolt;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.TopologyBuilder;
import backtype.storm.topology.base.BaseBasicBolt;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Tuple;
import backtype.storm.tuple.Values;

import java.util.HashMap;
import java.util.Map;

import storm.starter.spout.RandomPoints;

public class DenStream {
  public static class DenStreambolt extends ShellBolt implements IRichBolt {

    public DenStreambolt() {
      super("python", "denstreambolt.py");
    }

    @Override
    public void declareOutputFields(OutputFieldsDeclarer declarer) {
      declarer.declare(new Fields("point"));
    }

    @Override
    public Map<String, Object> getComponentConfiguration() {
      return null;
    }
  }

  public static void main(String[] args) throws Exception {

    TopologyBuilder builder = new TopologyBuilder();

    builder.setSpout("spout", new RandomPoints(), 5);

    builder.setBolt("denstreambolt", new DenStreambolt(), 1).shuffleGrouping("spout");

    Config conf = new Config();
    conf.setDebug(true);

    conf.setNumWorkers(1);

    StormSubmitter.submitTopology("DenStream", conf, builder.createTopology());

  }
}
